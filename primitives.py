import random

import pygame

from config import *
from utils import *


class Tile(pygame.sprite.Sprite):
    _walls = {
        Orient.UP: [(0, 1), (0, 2), (0, 3), (0, 4)],
        Orient.DOWN: [(4, 1), (4, 2), (4, 3), (4, 4)],
        Orient.LEFT: [(1, 0), (2, 0), (3, 0)],
        Orient.RIGHT: [(1, 4), (2, 4), (3, 4)],
        Orient.TOPLEFT: [(0, 0)],
        Orient.TOPRIGHT: [(0, 4)],
        Orient.BOTTOMLEFT: [(4, 0)],
        Orient.BOTTOMRIGHT: [(4, 4)],
    }

    def __init__(self, group=None, plane=0, x=0, y=0, mode='_', tileset=None):
        if group == None:
            super().__init__()
        else:
            super().__init__(group)
        self._p = plane
        self._x = x * TILE_SIZE
        self._y = y * TILE_SIZE
        self._mode = mode
        self._tileset = tileset

        self._empty = mode in ('.', '+', '_')
        self._orient = Orient.NONE
        self._image = self._get_image()
        self._rect = pygame.rect.Rect(self._x, self._y, TILE_SIZE, TILE_SIZE)
    
    def _get_image(self):
        if self._mode == "#":
            return get_image(self._tileset, 9, 6)
        elif self._mode == ".":
            return get_image(self._tileset, 9, 7)
        elif self._mode == "+":
            return get_square("white")
        elif self._mode == "R":
            return get_square("red")
        elif self._mode == "B":
            return get_square("blue")
        elif self._mode == "G":
            return get_square("green")
        elif self._mode == "Y":
            return get_square("yellow")
        else:
            return get_square("black")

    def set_orient(self, orient):
        self._orient = orient
        self._image = get_image(self._tileset, *random.choice(Tile._walls[self._orient]))
    
    def image(self):
        return self._image
    
    def rect(self):
        return self._rect
    
    def mode(self):
        return self._mode
    
    def is_empty(self):
        return self._empty


class World:
    def __init__(self, world, group=None, tileset=None):
        self._ps, self._w, self._h = len(world), len(world[0]), len(world[0][0])
        self._world = [
            [[Tile(group, p, j, i, world[p][i][j], tileset) for j in range(self._h)]
             for i in range(self._w)] for p in range(self._ps)
        ]
        for p in range(self._ps):
            self._orientate(self._world[p])
    
    def dim(self):
        return self._ps, self._w, self._h

    def __call__(self, *args, **kwds):
        return self._world
    
    def _orientate(self, plane):
        for y in range(self._h):
            for x in range(self._w):
                if not plane[y][x].is_empty():
                    plane[y][x].set_orient(self._orientate_tile(plane, x, y))
    
    def _orientate_tile(self, plane, x, y):
        # U D L R
        dx = (1, -1, 0, 0)
        dy = (0, 0, 1, -1)
        adj = [Tile() for _ in range(4)]
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if nx < 0 or nx >= self._w or ny < 0 or ny >= self._h:
                continue
            adj[i] = plane[ny][nx]
        if all([a.mode() == '.' for a in adj]):
            return Orient.CENTER
        if adj[0].mode() == '_' and adj[1].mode() == '.':
            return Orient.UP
        if adj[0].mode() == '.' and adj[1].mode() == '_':
            return Orient.DOWN
        if adj[2].mode() == '_' and adj[3].mode() == '.':
            return Orient.LEFT
        if adj[2].mode() == '.' and adj[3].mode() == '_':
            return Orient.RIGHT
        if not adj[1].is_empty() and not adj[3].is_empty():
            return Orient.TOPLEFT
        if not adj[1].is_empty() and not adj[2].is_empty():
            return Orient.TOPRIGHT
        if not adj[0].is_empty() and not adj[3].is_empty():
            return Orient.BOTTOMLEFT
        if not adj[0].is_empty() and not adj[2].is_empty():
            return Orient.BOTTOMRIGHT
        #TODO REST OF THE ITEMS, COLORED DOORS, CONNECTION UP, CONNECTION DOWN, ETC.

