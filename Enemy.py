import pygame

from config import *
from utils import *

from character import Character
from ss import Spritesheet


class Enemy(Character):
    def __init__(self, x, y, p, *groups):
        spritesheet = Spritesheet('Assets Folder/pp/Characters/Basic Charakter Spritesheet.png', 48)
        super().__init__(x, y, 3, spritesheet, *groups)
        self.image = get_square("red")
        self._p = p

    def update(self, game, *args, **kwargs):
        if self._p != game.p:
            return
        if (self.x, self.y) == (game.player.x, game.player.y):
            return
        path = game.world.pathfind(self._p, (self.x, self.y), (game.player.x, game.player.y))
        if path == None or len(path) < 2:
            return
        dx, dy = path[1][0] - self.x, path[1][1] - self.y
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