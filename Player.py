from config import *
from utils import *

import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        self.spritesheet = pygame.image.load("Assets Folder/Dungeon_Character_2.png").convert_alpha()
        self.image = get_image(self.spritesheet, 0, 0)
        self.x = x
        self.y = y
        self.scene_x = self.x * TILE_SIZE
        self.scene_y = self.y * TILE_SIZE
        self.size = TILE_SIZE
        self.spe = 3 * TILE_SIZE / BASE_SIZE
        self.rect = pygame.rect.Rect(self.scene_x, self.scene_y, self.size, self.size)
    
    def update(self, game, pressed, down):
        if pressed[K_UP]:
            self.scene_y -= self.spe
        if pressed[K_DOWN]:
            self.scene_y += self.spe
        if pressed[K_LEFT]:
            self.scene_x -= self.spe
        if pressed[K_RIGHT]:
            self.scene_x += self.spe
        self.scene_x = max(0, min(game.scene_w - self.size, self.scene_x))
        self.scene_y = max(0, min(game.scene_h - self.size, self.scene_y))

        self.x = int(self.scene_x // TILE_SIZE)
        self.y = int(self.scene_y // TILE_SIZE)
        
        self.rect = pygame.rect.Rect(self.scene_x, self.scene_y, self.size, self.size)
