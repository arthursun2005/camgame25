import pygame
from pygame.locals import *

from manual import *
from config import *
from utils import *
from title import *

from Player import Player
from primitives import Tile, World


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

        self.player = Player(1, 1)
        self.sprites.add(self.player)

    def get_cell(self, x, y):
        return self.world()[self.p][y][x]
    
    def spotlight(self,pos_tuple,size):
        x,y = pos_tuple
        filter = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)
        filter.fill(pygame.color.Color('Grey'))
        scaled_light = pygame.transform.scale(self.light,(self.light.get_width() * size,self.light.get_height() * size))
        sclight_width, sclight_height = scaled_light.get_size()
        light_rect = pygame.Rect(x-(sclight_width/2),y-(sclight_height/2),sclight_width,sclight_height)
        filter.blit(scaled_light,(x-(sclight_width / 2),y-(sclight_height/2),sclight_width,sclight_height))

        for obstacle in self.world.flatten(self.p):
            if obstacle.full():
                clip_rect = obstacle.rect.clip(light_rect)
                if clip_rect.width > 0 and clip_rect.height > 0:
                    # filter.fill((128,128,128,255),clip_rect)
                    pass
        self.screen.blit(filter,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
    
    def get_collision(self, base, sprites):
        collide = pygame.sprite.spritecollide(base, sprites, dokill=False)
        return collide

    def tile_collide(self, tile: Tile):
        if tile.not_wall():
            return False
        match tile.get_orient():
            case Orient.UP:
                self.player.scene_y = min(tile.rect.top, self.player.scene_y)

    def handle_player_collision(self):
        coll = self.get_collision(self.player, self.sprites)
        for obj in coll:
            if isinstance(obj, Tile):
                self.tile_collide(obj)

    def main(self):
        running = True
        self.init_World(MAP)
        self.lightRadius = 5
        while running:
            down = set()
            for event in pygame.event.get():
                self.title.process(event)
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    down.add(event.key)
                    if event.key == pygame.K_SPACE:
                        if self.get_cell(self.player.x, self.player.y + 1).mode() == '+':
                            self.p = (self.p + 1) % self.planes
            pressed = pygame.key.get_pressed()
            if pressed[K_g]:
                self.lightRadius = max(1, min(15, self.lightRadius + 0.5))
            if pressed[K_h]:
                self.lightRadius = max(1, min(15, self.lightRadius - 0.5))
            
            self.sprites.update(self, pressed, down)
            self.handle_player_collision()

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
                self.screen.blit(self.player.image, self.player.rect)
                self.spotlight(self.player.rect.center, self.lightRadius)

            pygame.display.flip()
            self.clock.tick(FPS)


game = Game()
game.main()
