import pygame
from pygame.locals import *

from manual import *
from config import *
from utils import *
from title import *

from Player import Player
from tile import Tile


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

    def main(self):
        running = True
        self.init_World(MAP)
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

            self.sprites.update(self, pressed, down)

            if not self.title.draw(self.screen):
                if self.ff:
                    self.music.stop()
                    self.music = pygame.mixer.Sound("Assets Folder/Music/Dream Sakura_Loop.ogg")
                    # self.music = pygame.mixer.Sound("Assets Folder/Music/Mysterious Kyoto.wav")
                    self.music.play(-1)
                    self.ff = False
                for y, row in enumerate(self.world[self.p]):
                    for x, cell in enumerate(row):
                        self.screen.blit(cell.image(), cell.rect())
                self.screen.blit(self.player.image, self.player.rect)

            pygame.display.flip()
            self.clock.tick(FPS)


game = Game()
game.main()
