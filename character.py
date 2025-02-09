from config import *
from utils import *
from ss import *
from animation import *

import pygame
from pygame.locals import *


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, spritesheet, *groups):
        super().__init__(*groups)
        self.size = TILE_SIZE * 4
        
        self.spritesheet = spritesheet
        self.image = pygame.transform.scale(self.spritesheet.get_image(0, 0), (self.size, self.size))

        self._brect_raw = self.image.get_bounding_rect()
        self.pady = (self.size - self._brect_raw.height) / 2
        self.padx = (self.size - self._brect_raw.width) / 2
        self.brect = self.image.get_bounding_rect()

        self.x = x
        self.y = y
        self.scene_x = self.x * TILE_SIZE - self.padx
        self.scene_y = self.y * TILE_SIZE - self.pady
        self.spe = speed * TILE_SIZE / BASE_SIZE
        self.set_brect()
        self.rect = pygame.rect.Rect(self.scene_x, self.scene_y, self.size, self.size)
        
        sps = self.spritesheet
        self.down = (Animation(sps, 5, [0, 1, 2, 3]), Animation(sps, 5, [0]))
        self.right = (Animation(sps, 5, [12, 13, 14, 15]), Animation(sps, 5, [12]))
        self.up = (Animation(sps, 5, [4, 5, 6, 7]), Animation(sps, 5, [4]))

        self.orit = 0
        self.moving = False
    
    def update(self, *args, **kwargs):
        self.x = max(0, min(WORLD_WIDTH * 2 - 1, int((self.scene_x + self.size / 2) // TILE_SIZE)))
        self.y = max(0, min(WORLD_HEIGHT * 2 - 1, int((self.scene_y + self.size / 2) // TILE_SIZE)))
        self.rect = self.image.get_rect(topleft=(self.scene_x, self.scene_y))
    
    def clip_top(self, y):
        self.scene_y = max(y - self.pady, self.scene_y)
    
    def clip_bot(self, y):
        self.scene_y = min(y - (self.size - self.pady), self.scene_y)
    
    def clip_left(self, x):
        self.scene_x = max(x - self.padx, self.scene_x)
    
    def clip_right(self, x):
        self.scene_x = min(x - (self.size - self.padx), self.scene_x)
    
    def set_brect(self):
        self.brect = pygame.rect.Rect(
            self.scene_x + self.padx,
            self.scene_y + self.pady,
            self._brect_raw.width,
            self._brect_raw.height
        )
