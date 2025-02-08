from enum import Enum


FPS = 60

TILE_DEPTH = 16 # size of tile in tile sheet
TILE_SIZE = 64 # size of tile in game

BASE_SIZE = 32

WORLD_WIDTH = 16
WORLD_HEIGHT = 16
SCREEN_WIDTH = TILE_SIZE * WORLD_WIDTH
SCREEN_HEIGHT = TILE_SIZE * WORLD_HEIGHT


class Orient(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    TOPLEFT = 5
    TOPRIGHT = 6
    BOTTOMLEFT = 7
    BOTTOMRIGHT = 8
    CENTER = 9
