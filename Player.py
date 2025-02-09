import time

from config import *
from utils import *
from ss import *
from animation import *

import pygame
from pygame.locals import *

from character import Character


class Player(Character):
    def __init__(self, x, y, *groups):
        spritesheet = Spritesheet('Assets Folder/pp/Characters/Basic Charakter Spritesheet.png', 48)
        super().__init__(x, y, PLAYER_SPEED, spritesheet, *groups)

        self.hp = 5
        
        sps = self.spritesheet
        self.down = (Animation(sps, 5, [0, 1, 2, 3]), Animation(sps, 5, [0]))
        self.right = (Animation(sps, 5, [12, 13, 14, 15]), Animation(sps, 5, [12]))
        self.up = (Animation(sps, 5, [4, 5, 6, 7]), Animation(sps, 5, [4]))

        self.orit = 0
        self.moving = False

        self.last_hit = 0
    
    def decrease_hp(self):
        now = time.time()
        if now - self.last_hit > HIT_COOLDOWN * 1000:
            self.hp -= 1
            self.last_hit = now
    
    def update_keys(self, game, pressed, down):
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

        self.scene_x = max(-self.padx, min(game.scene_w - (self.size - self.padx), self.scene_x))
        self.scene_y = max(-self.pady, min(game.scene_h - (self.size - self.pady), self.scene_y))

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
        self.image = pygame.transform.scale(img, (self.size, self.size))
        self.set_brect()
