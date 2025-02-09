import random
from collections import deque

import pygame

from config import *
from utils import *


class Tile(pygame.sprite.Sprite):
    _walls = {
        Orient.DOWN: [(0, 1), (0, 2), (0, 3), (0, 4)],
        Orient.UP: [(4, 1), (4, 2), (4, 3), (4, 4), (5, 1), (5, 2)],
        Orient.RIGHT: [(1, 0), (2, 0), (3, 0)],
        Orient.LEFT: [(1, 5), (2, 5), (3, 5)],
        Orient.BOTTOMRIGHT_IN: [(0, 0)],
        Orient.BOTTOMLEFT_IN: [(0, 5)],
        Orient.TOPRIGHT_IN: [(4, 0)],
        Orient.TOPLEFT_IN: [(4, 5)],
        Orient.BOTTOMRIGHT_OUT: [(0, 1), (0, 2), (0, 3), (0, 4)],
        Orient.BOTTOMLEFT_OUT: [(0, 1), (0, 2), (0, 3), (0, 4)],
        Orient.TOPRIGHT_OUT: [(5, 3), (5, 5)],
        Orient.TOPLEFT_OUT: [(5, 0), (5, 4)],
        Orient.SURROUNDED: [(7, 8)]
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

        self._isconn = mode in ('0', '1', '2')
        self._conn = int(mode) if self._isconn else None
        self._empty = mode == '.' or self._isconn
        self._notwall = mode in ('.', '_') or self._isconn
        self._truewall = mode == '#'
        self._orient = Orient.NONE
        
        self.image = self._get_image()
        self.rect = self.image.get_rect(topleft=(self._x, self._y))
        # pygame.rect.Rect(self._x, self._y, TILE_SIZE, TILE_SIZE)
    
    def _get_image(self):
        if self._mode == "#":
            return get_image(self._tileset, 9, 6)
        elif self._mode == ".":
            return get_image(self._tileset, 9, 7)
        elif self._isconn:
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
        self.image = get_image(self._tileset, x, y)
    
    def get_orient(self):
        return self._orient
    
    def mode(self):
        return self._mode
    
    def not_wall(self):
        """Return True if non-wall tile (including invalid tiles)"""
        return self._notwall
    
    def empty(self):
        """Return True if non-wall tile (excluding invalid tiles)"""
        return self._empty
    
    def full(self):
        """Return True if wall/door tile (excluding invalid tiles)"""
        return not self._notwall
    
    def truewall(self):
        """Return True if actual wall tile"""
        return self._truewall

    def invalid(self):
        """Return True if invalid tile"""
        return self._mode == '_'
    
    def isconn(self):
        """Return True if connection"""
        return self._isconn
    
    def conn(self):
        """Return index of connected plane"""
        return self._conn


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

    _orig_to_world = {
        OrigOrient.HORIZONTAL: [Orient.UP, Orient.UP, Orient.DOWN, Orient.DOWN],
        OrigOrient.VERTICAL: [Orient.LEFT, Orient.RIGHT, Orient.LEFT, Orient.RIGHT],
        OrigOrient.TOPLEFT: [Orient.TOPLEFT_OUT, Orient.UP, Orient.LEFT, Orient.BOTTOMRIGHT_IN],
        OrigOrient.TOPRIGHT: [Orient.UP, Orient.TOPRIGHT_OUT, Orient.BOTTOMLEFT_IN, Orient.RIGHT],
        OrigOrient.BOTTOMLEFT: [Orient.LEFT, Orient.TOPRIGHT_IN, Orient.BOTTOMLEFT_OUT, Orient.DOWN],
        OrigOrient.BOTTOMRIGHT: [Orient.TOPLEFT_IN, Orient.RIGHT, Orient.DOWN, Orient.BOTTOMRIGHT_OUT],
        OrigOrient.TOP_T: [Orient.UP, Orient.UP, Orient.BOTTOMLEFT_IN, Orient.BOTTOMRIGHT_IN],
        OrigOrient.BOTTOM_T: [Orient.TOPLEFT_IN, Orient.TOPRIGHT_IN, Orient.DOWN, Orient.DOWN],
        OrigOrient.LEFT_T: [Orient.LEFT, Orient.TOPRIGHT_IN, Orient.LEFT, Orient.BOTTOMRIGHT_IN],
        OrigOrient.RIGHT_T: [Orient.TOPLEFT_IN, Orient.RIGHT, Orient.BOTTOMLEFT_IN, Orient.RIGHT],
        OrigOrient.LEFT_END: [Orient.TOPLEFT_OUT, Orient.UP, Orient.BOTTOMLEFT_OUT, Orient.DOWN],
        OrigOrient.RIGHT_END: [Orient.UP, Orient.TOPRIGHT_OUT, Orient.DOWN, Orient.BOTTOMRIGHT_OUT],
        OrigOrient.TOP_END: [Orient.TOPLEFT_OUT, Orient.TOPRIGHT_OUT, Orient.LEFT, Orient.RIGHT],
        OrigOrient.BOTTOM_END: [Orient.LEFT, Orient.RIGHT, Orient.BOTTOMLEFT_OUT, Orient.BOTTOMRIGHT_OUT],
        OrigOrient.CENTER: [Orient.TOPLEFT_OUT, Orient.TOPRIGHT_OUT, Orient.BOTTOMLEFT_OUT, Orient.BOTTOMRIGHT_OUT],
        OrigOrient.SURROUNDED: [Orient.TOPLEFT_IN, Orient.TOPRIGHT_IN, Orient.BOTTOMLEFT_IN, Orient.BOTTOMRIGHT_IN]
    }

    def __init__(self, world, group=None, tileset=None):
        self._ps, self._w, self._h = len(world), len(world[0][0]) * 2, len(world[0]) * 2
        self._orig = [
            [[Tile(None, p, j, i, world[p][i][j], tileset) for j in range(self._w // 2)]
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
                    if not self._world[p][y][x].full():
                        continue
                    self._world[p][y][x].set_orient(self._orient_tile(p, x, y))
        for p in range(self._ps):
            for y in range(self._h):
                for x in range(self._w):
                    if not self._world[p][y][x].full():
                        continue
                    self._orient_surrounded(p, x, y)
    
    def __call__(self, *args, **kwds):
        return self._world

    def flatten(self, p):
        arr = []
        for row in self._world[p]:
            for cell in row:
                arr.append(cell)
        return arr
    
    def within_dist(self, p, dist, center):
        cx, cy = center
        arr = []
        for y in range(max(0, cy - dist), min(self._h, cy + dist + 1)):
            arr.extend(self._world[p][y][max(0, cx - dist): min(self._w, cx + dist + 1)])
        return arr

    def dim(self):
        return self._ps, self._w, self._h
    
    def pathfind(self, p, src, dst):
        dx = (0, 0, -1, 1)
        dy = (-1, 1, 0, 0)
        q = deque()
        d = [[1e9+7 for _ in range(self._w)] for _ in range(self._h)]
        par = [[(0, 0) for _ in range(self._w)] for _ in range(self._h)]
        q.append((src[1], src[0]))
        d[src[1]][src[0]] = 0
        while q:
            y, x = q.popleft()
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if nx < 0 or nx >= self._w or ny < 0 or ny >= self._h:
                    continue
                if not self._world[p][ny][nx].empty():
                    continue
                if d[y][x] + 1 < d[ny][nx]:
                    d[ny][nx] = d[y][x] + 1
                    par[ny][nx] = (x, y)
                    q.append((ny, nx))
        if d[dst[1]][dst[0]] == 1e9+7:
            return None
        res = [dst]
        x, y = dst
        while par[y][x] != src:
            x, y = par[y][x]
            res.append((x, y))
        res.reverse()
        return res

    def closest_door(self, p, src):
        dx = (0, 0, -1, 1)
        dy = (-1, 1, 0, 0)
        q = deque()
        d = [[1e9+7 for _ in range(self._w)] for _ in range(self._h)]
        par = [[(0, 0) for _ in range(self._w)] for _ in range(self._h)]
        q.append((src[1], src[0]))
        d[src[1]][src[0]] = 0
        while q:
            y, x = q.popleft()
            for i in range(4):
                nx, ny = x + dx[i], y + dy[i]
                if nx < 0 or nx >= self._w or ny < 0 or ny >= self._h:
                    continue
                if not self._world[p][ny][nx].empty():
                    continue
                if d[y][x] + 1 < d[ny][nx]:
                    d[ny][nx] = d[y][x] + 1
                    par[ny][nx] = (x, y)
                    q.append((ny, nx))

    def get_empty_cell(self, p):
        calls = 0
        while calls < 1000:
            x = random.randint(0, self._w - 1)
            y = random.randint(0, self._h - 1)
            if self._world[p][y][x].empty():
                return (x, y)
        return (-1, -1)

    def _get_adj(self, plane, x, y):
        dx = (0, 0, -1, 1, -1, -1, 1, 1)
        dy = (-1, 1, 0, 0, -1, 1, -1, 1)
        wmap = ('U', 'D', 'L', 'R', 'UL', 'UR', 'DL', 'DR')
        adj = {}
        for i in range(len(dx)):
            nx, ny = x + dx[i], y + dy[i]
            if nx < 0 or nx >= len(plane[0]) or ny < 0 or ny >= len(plane):
                adj[wmap[i]] = Tile()
                continue
            adj[wmap[i]] = plane[ny][nx]
        return adj
    
    def _adj_orig_format(self, adj):
        arr = []
        for a in adj:
            if a in ('U', 'D', 'L', 'R'):
                arr.append(adj[a].full())
        return tuple(arr)

    def _orient_orig(self, plane, x, y):
        adj = self._adj_orig_format(self._get_adj(plane, x, y))
        return World._orig_map[adj]

    def _orient_tile(self, p, x, y):
        tx, cx = divmod(x, 2)
        ty, cy = divmod(y, 2)
        tile_pos = cy * 2 + cx
        orig_orient = self._orig_orient[p][ty][tx]
        world_orient = World._orig_to_world[orig_orient][tile_pos]
        return world_orient
    
    def _orient_surrounded(self, p, x, y):
        adj = self._get_adj(self._world[p], x, y)
        if all([a.full() for a in adj.values()]):
            self._world[p][y][x].set_orient(Orient.SURROUNDED)
