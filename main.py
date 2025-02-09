from collections import deque
import time

import pygame
import math
from pygame.locals import *

from manual import *
from config import *
from utils import *
from title import *

from Player import Player
from Enemy import Enemy
from primitives import Tile, World
from genmaze import genmaze


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        try:
            pygame.mixer.init()
            # self.music = pygame.mixer.Sound("Assets Folder/Music/Dream Sakura_Loop.ogg")
            self.music = pygame.mixer.Sound("Assets Folder/Music/Mysterious Kyoto.wav")
            self.music.play(-1)
        except:
            pass
        
        self.tileset = pygame.image.load("Assets Folder/Dungeon_Tileset.png").convert_alpha()
        self.light = pygame.image.load("Assets Folder/spotlight.png").convert_alpha()
        
        self.world = None
        self.p = None
        self.planes = None
        self.width = None
        self.height = None
        self.scene_w = None
        self.scene_h = None

        self.sprites = None
        self.player = None

        self.title = Title()
        self.ff = True

    def init_World(self, world):
        self.sprites = pygame.sprite.Group()
        self.world = World(world, self.sprites, self.tileset)
        self.planes, self.width, self.height = self.world.dim()
        
        self.scene_w, self.scene_h = self.width * TILE_SIZE, self.height * TILE_SIZE
        self.p = 0 # current plane

        self.player = Player(4, 6)
        self.sprites.add(self.player)

    def get_cell(self, x, y):
        try:
            return self.world()[self.p][y][x]
        except IndexError:
            return Tile()
    
    def spotlight(self,pos_tuple,size):
        x,y = pos_tuple
        filter = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)
        filter.fill(pygame.color.Color('grey'))
        scaled_light = pygame.transform.scale(self.light,(self.light.get_width() * size,self.light.get_height() * size))
        sclight_width, sclight_height = scaled_light.get_size()
        light_rect = pygame.Rect(x-(sclight_width/2),y-(sclight_height/2),sclight_width,sclight_height)
        filter.blit(scaled_light,(x-(sclight_width / 2),y-(sclight_height/2),sclight_width,sclight_height))
        self.screen.blit(filter,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
    
    def ray_intersections(self,angleInc,lightRadius):
        collisionPoints = []
        for angle in range(0,360,angleInc):
            radians = math.radians(angle)
            dx = math.cos(radians)
            dy = math.sin(radians)
            rayEnd = (self.player.rect.center[0] + (dx * lightRadius), self.player.rect.center[1] + (dy *lightRadius))
            closest_hit = None
            for obstacle in self.world.within_dist(self.p, 4, (self.player.x,self.player.y)):
                if obstacle.full():
                    obRect = obstacle.rect
                    for edge in [
                        (obRect.topleft,obRect.topright),
                        (obRect.topright,obRect.bottomright),
                        (obRect.bottomright,obRect.bottomleft),
                        (obRect.bottomleft,obRect.topleft)]:
                        hit = line_intersect(self.player.rect.center,rayEnd,edge[0],edge[1])
                        if hit != None:
                            if closest_hit is None or distance(self.player.rect.center,hit) < distance(self.player.rect.center,closest_hit):
                                closest_hit = hit
                        
            collisionPoints.append(closest_hit if closest_hit != None else rayEnd)
        return collisionPoints
    
    def cast_light(self,angleInc,lightRadius):
        filter = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)
        filter.fill(pygame.color.Color('White'))
        filter.fill(pygame.color.Color('White'))
        pygame.draw.polygon(filter,(15,15,15,200),self.ray_intersections(angleInc,lightRadius))
        self.screen.blit(filter,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
        for points in self.ray_intersections(angleInc,lightRadius):
             pygame.draw.circle(self.screen, (255, 0, 0), points, 1)

    
    def get_collision(self, base, sprites):
        collide = pygame.sprite.spritecollide(base, sprites, dokill=False)
        return collide

    def tile_collide(self, tile: Tile):
        if tile.not_wall() or tile._p != self.p:
            return False
        colls = collision(self.player.brect, tile.rect)
        if Collision.TOP in colls:
            self.player.clip_top(tile.rect.bottom)
        if Collision.BOTTOM in colls:
            self.player.clip_bot(tile.rect.top)
        if Collision.LEFT in colls:
            self.player.clip_left(tile.rect.right)
        if Collision.RIGHT in colls:
            self.player.clip_right(tile.rect.left)
        return Collision.NONE not in colls

    def handle_player_collision(self, down):
        coll = self.get_collision(self.player, self.sprites)
        self.buf = []
        for obj in coll:
            if isinstance(obj, Tile):
                if obj.isdoor():
                    if K_1 in down and obj.mode() == 'r':
                        obj = Tile(mode='.')
                    if K_2 in down and obj.mode() == 'g':
                        obj = Tile(mode='.')
                    if K_3 in down and obj.mode() == 'b':
                        obj = Tile(mode='.')
                if self.tile_collide(obj):
                    self.player.set_brect()
                    self.buf.append(obj)
            if isinstance(obj, Enemy):
                if collision(self.player.brect, obj.brect):
                    if K_q in down:
                        obj.decrease_hp(self)
                    self.player.decrease_hp()

    def set_lightradius(self, radius):
        self.lightRadius = max(MIN_LIGHT, min(MAX_LIGHT, radius))

    def spawn_enemy(self):
        x, y = self.world.get_empty_cell(self.p)
        if (x, y) != (-1, -1):
            return Enemy(x, y, self.p, self.enemies, self.sprites)

    def door_lights(self):
        lights_to_kill = 0
        # print(self.spotlights)
        for light, tm in self.spotlights:
            if time.time() - tm > DOOR_LIGHT_LIFE:
                lights_to_kill += 1
            else:
                # for cell in self.world.within_dist(self.p, 1, (light._x // TILE_SIZE, light._y // TILE_SIZE)):
                #     self.screen.blit(cell.image, cell.rect)
                self.spotlight((light._x, light._y), DOOR_LIGHT)
        for light in range(lights_to_kill):
            self.spotlights.popleft()

    def main(self, debug=False):
        running = True
        self.init_World(genmaze(False))
        self.lightRadius = 100
        self.buf = []
        self.enemies = pygame.sprite.Group()
        self.spotlights = deque()
        for _ in range(MAX_ENEMIES):
            self.spawn_enemy()
        while running:
            self.cursl = None
            self.screen.fill((30,30,30)) # Used for the lighting
            down = set()
            for event in pygame.event.get():
                self.title.process(event)
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    down.add(event.key)
                    if event.key == pygame.K_SPACE:
                        cell = self.get_cell(self.player.x, self.player.y)
                        if cell.isconn():
                            self.p = cell.conn()
            pressed = pygame.key.get_pressed()
            if pressed[K_g]:
                self.lightRadius = max(MIN_LIGHT, min(MAX_LIGHT, self.lightRadius + DELTA_LIGHT))
            if pressed[K_h]:
                self.lightRadius = max(MIN_LIGHT, min(MAX_LIGHT, self.lightRadius - DELTA_LIGHT))
            
            self.player.update_keys(self, pressed, down)
            self.handle_player_collision(down)
            if len(self.enemies) < MAX_ENEMIES:
                self.spawn_enemy()
            self.sprites.update(self)
            
            # self.set_lightradius(self.player.hp * 10)
            if self.cursl != None:
                ok = True
                for light, _ in self.spotlights:
                    if light == self.cursl:
                        ok = False
                        break
                if ok:
                    self.spotlights.append((self.cursl, time.time()))

            if not self.title.draw(self.screen):
                if self.ff:
                    self.music.stop()
                    self.music = pygame.mixer.Sound("Assets Folder/Music/Dream Sakura_Loop.ogg")
                    # self.music = pygame.mixer.Sound("Assets Folder/Music/Mysterious Kyoto.wav")
                    self.music.play(-1)
                    self.ff = False
                for y, row in enumerate(self.world()[self.p]):
                    for x, cell in enumerate(row):
                        self.screen.blit(cell.image, cell.rect)

                for enemy in self.enemies:
                    self.screen.blit(enemy.image, enemy.rect)
                self.screen.blit(self.player.image, self.player.rect)
                #self.spotlight(self.player.rect.center, self.lightRadius)
                
                self.cast_light(10, self.lightRadius)
                self.door_lights()
            
            if debug:
                pygame.draw.rect(self.screen, "red", self.player.brect, width=1)
                pygame.draw.rect(self.screen, "blue", self.player.rect, width=1)
                for obj in self.buf:
                    pygame.draw.rect(self.screen, "green", obj.rect, width=1)
            
            pygame.display.flip()
            self.clock.tick(FPS)


game = Game()
game.main(debug=False)
