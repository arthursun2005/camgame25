import random
import time

import pygame

from config import *
from utils import *

from character import Character
from ss import Spritesheet
from animation import Animation

from tone import generate_tune
import numpy as np


class Enemy(Character):
    def __init__(self, x, y, p, *groups):
        spritesheet = Spritesheet('Assets Folder/pp/Characters/Basic Charakter Spritesheet.png', 48)
        super().__init__(x, y, ENEMY_SPEED, spritesheet, *groups)
        self._p = p

        sps = self.spritesheet
        self.down = (Animation(sps, 5, [0, 1, 2, 3]), Animation(sps, 5, [0]))
        self.right = (Animation(sps, 5, [12, 13, 14, 15]), Animation(sps, 5, [12]))
        self.up = (Animation(sps, 5, [4, 5, 6, 7]), Animation(sps, 5, [4]))

        self.orit = 0
        self.moving = False

        self.last_check = time.time()
        self.lifetime = random.randint(MIN_LIFETIME, MAX_LIFETIME)

        self.hp = 3

    def update(self, game, *args, **kwargs):
        # print(time.time() - self.last_check)
        if time.time() - self.last_check > self.lifetime:
            self.kill()
        if self._p != game.p:
            return
        if (self.x, self.y) == (game.player.x, game.player.y):
            return
        path = game.world.pathfind(self._p, (self.x, self.y), (game.player.x, game.player.y))
        if path == None or len(path) > MAX_AGGRO:
            return
        if len(path) < 2:
            dx, dy = game.player.scene_x - self.scene_x, game.player.scene_y - self.scene_y
        else:
            dx, dy = path[1][0] - self.x, path[1][1] - self.y
        self.last_check = time.time()
        self.update_pos(game, dx, dy)
        super().update()
    
    def update_pos(self, game, dx, dy):
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

    def decrease_hp(self, game):
        self.hp -= 1
        if self.hp <= 0:
            door = game.world.closest_door(self._p, (self.x, self.y))
            
            if door != None:
                if door.mode() == 'R':
                    buffer = np.int16(generate_tune('piano', sec=0.6) * 0.3 * (2**15-1))
                    buffer = np.tile(buffer[:, None], (1, 2))

                    sound = pygame.sndarray.make_sound(buffer)
                    sound.play()
                    pass #TODO: play piano
                elif door.mode() == 'G':
                    buffer = np.int16(generate_tune('violin', sec=1) * 0.3 * (2**15-1))
                    buffer = np.tile(buffer[:, None], (1, 2))
                    sound = pygame.sndarray.make_sound(buffer)
                    sound.play()
                    
                    pass #TODO: play violin
                elif door.mode() == 'B':
                    buffer = np.int16(generate_tune('flute', sec=1) * 0.3 * (2**15-1))
                    buffer = np.tile(buffer[:, None], (1, 2))

                    sound = pygame.sndarray.make_sound(buffer)
                    sound.play()

                    pass #TODO: play flute
                game.cursl = door
            self.kill()