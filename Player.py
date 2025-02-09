from config import *
from utils import *
from ss import *
from animation import *

import pygame
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        # self.spritesheet = pygame.image.load("Assets Folder/Dungeon_Character_2.png").convert_alpha()
        # self.image = get_image(self.spritesheet, 0, 0)
        self.spritesheet = Spritesheet('Assets Folder/pp/Characters/Basic Charakter Spritesheet.png', 48)
        self.image = pygame.transform.scale(self.spritesheet.get_image(0, 0), (TILE_SIZE, TILE_SIZE))
        self.x = x
        self.y = y
        self.scene_x = self.x * TILE_SIZE
        self.scene_y = self.y * TILE_SIZE
        self.size = TILE_SIZE
        self.spe = 3 * TILE_SIZE / BASE_SIZE
        self.rect = pygame.rect.Rect(self.scene_x, self.scene_y, self.size, self.size)
        
        sps = self.spritesheet
        self.down = (Animation(sps, 5, [0, 1, 2, 3]), Animation(sps, 5, [0]))
        self.right = (Animation(sps, 5, [12, 13, 14, 15]), Animation(sps, 5, [12]))
        self.up = (Animation(sps, 5, [4, 5, 6, 7]), Animation(sps, 5, [4]))

        self.orit = 0
        self.moving = False
    
    def update(self, game, pressed, down):
        dx, dy = 0, 0
        if pressed[K_UP] or pressed[K_w]:
            dy -= self.spe
        if pressed[K_DOWN] or pressed[K_s]:
            dy += self.spe
        if pressed[K_LEFT] or pressed[K_a]:
            dx -= self.spe
        if pressed[K_RIGHT] or pressed[K_d]:
            dx += self.spe
        r = (dx ** 2 + dy ** 2) ** 0.5
        dx *= self.spe / (r + 1e-6)
        dy *= self.spe / (r + 1e-6)
        self.scene_x += dx
        self.scene_y += dy
        if abs(dx) + abs(dy) > 0:
            self.moving = True
        else:
            self.moving = False

        if dx > 0:
            self.orit = 0
        elif dy < 0:
            self.orit = 1
        elif dx < 0:
            self.orit = 2
        elif dy > 0:
            self.orit = 3

        self.scene_x = max(0, min(game.scene_w - self.size, self.scene_x))
        self.scene_y = max(0, min(game.scene_h - self.size, self.scene_y))

        self.x = int(self.scene_x // TILE_SIZE)
        self.y = int(self.scene_y // TILE_SIZE)

        ii = not self.moving
        if self.orit == 0:
            img = self.right[ii].get_image()
        if self.orit == 1:
            img = self.up[ii].get_image()
        if self.orit == 2:
            img = self.right[ii].get_image()
            img = pygame.transform.flip(img, 1, 0)
        if self.orit == 3:
            img = self.down[ii].get_image()
        self.image = pygame.transform.scale(img, (TILE_SIZE * 2, TILE_SIZE * 2))
        # self.rect = pygame.rect.Rect(self.scene_x, self.scene_y, self.size, self.size)
        self.rect = self.image.get_rect(center=(self.scene_x, self.scene_y))
