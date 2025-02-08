import pygame

from config import *


class Tile:
    def __init__(self, image=pygame.surface.Surface((0, 0)), x=0, y=0, mode="#"):
        self._image = image
        self._x = x * TILE_SIZE
        self._y = y * TILE_SIZE
        self._mode = mode
        self._rect = pygame.rect.Rect(self._x, self._y, TILE_SIZE, TILE_SIZE)
    
    def image(self):
        return self._image
    
    def rect(self):
        return self._rect
    
    def mode(self):
        return self._mode