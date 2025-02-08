import pygame
from pygame.locals import *
from manual import TEST
from config import *


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game:
    def __init__(self):
        self.in_dialogue = False
        self.tileset = pygame.image.load("Assets Folder\Dungeon_Tileset.png").convert_alpha()
        self.spritesheet = pygame.image.load("Assets Folder\Dungeon_Character_2.png").convert_alpha()
        try:
            pygame.mixer.init()
            self.music = pygame.mixer.Sound("assets/music/m.wav")
            self.music.play(-1)
        except:
            pass
    
    def init_World(self, world):
        self.world = [[self.arrValue(world[i][j]) for j in range(len(world))] for i in range(len(world[0]))]
    
    def arrValue(self,item):
        if item == "#":
            return self.get_image(9,6)
        elif item == ".":
            return self.get_image(9,7)
        #TODO REST OF THE ITEMS, COLORED DOORS, CONNECTION UP, CONNECTION DOWN, ETC.

    def get_image(self, x, y):
        sprite = pygame.Surface((TILE_DEPTH, TILE_DEPTH), pygame.SRCALPHA, 32).convert_alpha()
        sprite.blit(self.tileset, (0, 0), 
                    (x * TILE_DEPTH, y * TILE_DEPTH, TILE_DEPTH, TILE_DEPTH))
        sprite = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
        return sprite
    
    def main(self):
        running = True
        self.init_World(TEST)
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            for y, row in enumerate(self.world):
                for x, cell in enumerate(row):
                    screen.blit(cell, pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, (x+1)*TILE_SIZE, (y+1)*TILE_SIZE))

            pygame.display.flip()
    

game = Game()
game.main()