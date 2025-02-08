import random

import pygame

from config import *
from utils import *


class Tile(pygame.sprite.Sprite):
    _walls = {
        Orient.UP: [(0, 1), (0, 2), (0, 3), (0, 4)],
        Orient.DOWN: [(4, 1), (4, 2), (4, 3), (4, 4)],
        Orient.LEFT: [(1, 0), (2, 0), (3, 0)],
        Orient.RIGHT: [(1, 5), (2, 5), (3, 5)],
        Orient.TOPLEFT: [(0, 0)],
        Orient.TOPRIGHT: [(0, 5)],
        Orient.BOTTOMLEFT: [(4, 0)],
        Orient.BOTTOMRIGHT: [(4, 5)],
        Orient.CENTER: [(4, 5)]
    }

    def __init__(self, group=None, plane=0, x=0, y=0, mode='_', tileset=None):
        """Default mode '_' = invalid tile"""

        if group == None:
            super().__init__()
        else:
            super().__init__(group)
        self._p = plane
        self._x = x * TILE_SIZE
        self._y = y * TILE_SIZE
        self._mode = mode
        self._tileset = tileset

        self._notwall = mode in ('.', '+', '_')
        self._empty = mode in ('.', '+')
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
        y, x = random.choice(Tile._walls[self._orient])
        self._image = get_image(self._tileset, x, y)
    
    def image(self):
        return self._image
    
    def rect(self):
        return self._rect
    
    def mode(self):
        return self._mode
    
    def not_wall(self):
        """Return True if non-wall tile (including invalid tiles)"""
        return self._notwall
    
    def empty(self):
        """Return True if non-wall tile (excluding invalid tiles)"""
        return self._empty
    
    def full(self):
        """Return True if wall tile (excluding invalid tiles)"""
        return not self._notwall

    def invalid(self):
        """Return True if invalid tile"""
        return self._mode == '_'


class World:
    _orig_map = {
        (0, 0, 1, 1): OrigOrient.HORIZONTAL,
        (1, 1, 0, 0): OrigOrient.VERTICAL,
        (0, 1, 0, 1): OrigOrient.TOPLEFT,
        (0, 1, 1, 0): OrigOrient.TOPRIGHT,
        (1, 0, 0, 1): OrigOrient.BOTTOMLEFT,
        (1, 0, 1, 0): OrigOrient.BOTTOMRIGHT,
        (0, 1, 1, 1): OrigOrient.TOP_T,
        (1, 0, 1, 1): OrigOrient.BOTTOM_T,
        (1, 1, 0, 1): OrigOrient.LEFT_T,
        (1, 1, 1, 0): OrigOrient.RIGHT_T,
        (0, 0, 0, 1): OrigOrient.LEFT_END,
        (0, 0, 1, 0): OrigOrient.RIGHT_END,
        (0, 1, 0, 0): OrigOrient.TOP_END,
        (1, 0, 0, 0): OrigOrient.BOTTOM_END,
        (0, 0, 0, 0): OrigOrient.CENTER,
        (1, 1, 1, 1): OrigOrient.SURROUNDED
    }

    def __init__(self, world, group=None, tileset=None):
        self._ps, self._w, self._h = len(world), len(world[0][0]) * 2, len(world[0]) * 2
        self._orig = [
            [[Tile(group, p, j, i, world[p][i][j], tileset) for j in range(self._w // 2)]
             for i in range(self._h // 2)] for p in range(self._ps)
        ]
        self._orig_orient = [[[OrigOrient.NONE for _ in range(len(world[0][0]))]
                              for _ in range(len(world[0]))] for _ in range(len(world))]
        
        self._world = [
            [[Tile(group, p, j, i, world[p][i // 2][j // 2], tileset) for j in range(self._w)]
             for i in range(self._h)] for p in range(self._ps)
        ]
        for p in range(self._ps):
            for y in range(self._h // 2):
                for x in range(self._w // 2):
                    self._orig_orient[p][y][x] = self._orient_orig(self._orig[p], x, y)
        for p in range(self._ps):
            for y in range(self._h):
                for x in range(self._w):
                    self._world[p][y][x].set_orient(self._orient_tile(self._world[p], x, y))
    
    def dim(self):
        return self._ps, self._w, self._h
    
    def _get_adj(self, plane, x, y):
        dx = (0, 0, -1, 1)
        dy = (-1, 1, 0, 0)
        wmap = ('U', 'D', 'L', 'R')
        adj = {}
        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if nx < 0 or nx >= len(plane[0]) or ny < 0 or ny >= len(plane):
                adj[wmap[i]] = Tile()
                continue
            adj[wmap[i]] = plane[ny][nx]
        return adj
    
    def _adj_orig_format(self, adj):
        return tuple([a.full() for a in adj.values()])

    def _orient_orig(self, plane, x, y):
        adj = self._adj_orig_format(self._get_adj(plane, x, y))
        return World._orig_map[adj]

    def __call__(self, *args, **kwds):
        return self._world
    
    def _orientate(self, plane):
        for y in range(self._h):
            for x in range(self._w):
                if not plane[y][x].not_wall():
                    plane[y][x].set_orient(self._orient_tile(plane, x, y))
    
    def _get_corner(self, x, y):
        return (x % 2, y % 2)

    def _orient_tile(self, plane, x, y):
        match self._orig
        adj = self._get_adj(plane, x, y)
        if all([a.empty() for a in adj.values()]):
            return Orient.CENTER
        if adj[0].invalid() and adj[1].empty():
            return Orient.UP
        if adj[0].empty() and adj[1].invalid():
            return Orient.DOWN
        if adj[2].invalid() and adj[3].empty():
            return Orient.LEFT
        if adj[2].empty() and adj[3].invalid():
            return Orient.RIGHT
        if not adj[1].not_wall() and not adj[3].not_wall():
            return Orient.TOPLEFT
        if not adj[1].not_wall() and not adj[2].not_wall():
            return Orient.TOPRIGHT
        if not adj[0].not_wall() and not adj[3].not_wall():
            return Orient.BOTTOMLEFT
        if not adj[0].not_wall() and not adj[2].not_wall():
            return Orient.BOTTOMRIGHT
        return Orient.UP
        #TODO REST OF THE ITEMS, COLORED DOORS, CONNECTION UP, CONNECTION DOWN, ETC.

