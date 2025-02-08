import pygame
from pygame.locals import *

from manual import *
from config import *
from utils import *

from Player import Player
from tile import Tile


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        try:
            pygame.mixer.init()
            self.music = pygame.mixer.Sound("assets/music/m.wav")
            self.music.play(-1)
        except:
            pass
        
        self.tileset = pygame.image.load("Assets Folder\Dungeon_Tileset.png").convert_alpha()
        self.light = pygame.image.load("Assets Folder\spotlight.png").convert_alpha()

        self.world = None
        self.p = None
        self.planes = None
        self.width = None
        self.height = None
        self.scene_w = None
        self.scene_h = None

        self.sprites = None
        self.player = None

    
    def init_World(self, world):
        self.planes, self.width, self.height = len(world), len(world[0]), len(world[0][0])
        self.scene_w, self.scene_h = self.width * TILE_SIZE, self.height * TILE_SIZE

        self.world = [
            [[Tile(self.arrValue(world[p][i][j],p), j, i, world[p][i][j]) for j in range(self.height)]
             for i in range(self.width)] for p in range(self.planes)
        ]
        self.p = 0 # current plane

        self.sprites = pygame.sprite.Group()
        self.player = Player(1, 1)
        self.sprites.add(self.player)
    
    def arrValue(self,item,p):
        if item == "#":
            return get_image(self.tileset, 9, 6)
        elif item == ".":
            return get_image(self.tileset, 9, 7)
        elif item == "+":
            if p == 0:
                return get_image(self.tileset,9,0)
            elif p == 1:
                return get_image(self.tileset,8,0)
            elif p == 2:
                return get_image(self.tileset,7,0)
        elif item == "R":
            return get_square("red")
        elif item == "B":
            return get_square("blue")
        elif item == "G":
            return get_square("green")
        elif item == "Y":
            return get_square("yellow")
        else:
            return get_square("black")
        #TODO REST OF THE ITEMS, COLORED DOORS, CONNECTION UP, CONNECTION DOWN, ETC.

    def get_cell(self, x, y):
        return self.world[self.p][y][x]
    
    def spotlight(self,pos_tuple,size):
        x,y = pos_tuple
        filter = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        filter.fill(pygame.color.Color('Grey'))
        scaled_light = pygame.transform.scale(self.light,(self.light.get_width() * size,self.light.get_height() * size))
        sclight_width, sclight_height = scaled_light.get_size()
        filter.blit(scaled_light,(x-(sclight_width / 2),y-(sclight_height/2)))
        self.screen.blit(filter,(0,0),special_flags=pygame.BLEND_RGBA_SUB)

    def main(self):
        running = True
        self.init_World(MAP)
        self.lightRadius = 5
        while running:
            down = set()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    down.add(event.key)
                    if event.key == pygame.K_SPACE:
                        if self.get_cell(self.player.x, self.player.y + 1).mode() == '+':
                            self.p = (self.p + 1) % self.planes
            pressed = pygame.key.get_pressed()
            if pressed[K_a]:
                self.lightRadius += 0.5

            self.sprites.update(self, pressed, down)

            for y, row in enumerate(self.world[self.p]):
                for x, cell in enumerate(row):
                    self.screen.blit(cell.image(), cell.rect())
            self.screen.blit(self.player.image, self.player.rect)
            self.spotlight(self.player.rect.center,self.lightRadius)

            pygame.display.flip()
            self.clock.tick(FPS)


game = Game()
game.main()
