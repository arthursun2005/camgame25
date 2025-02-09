from enum import Enum

FPS = 60

TILE_DEPTH = 16 # size of tile in tile sheet
TILE_SIZE = 48 # size of tile in game

BASE_SIZE = 32

WORLD_WIDTH = 16
WORLD_HEIGHT = 16
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1200 # arthur's screen lmao
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720 # karp's screen lmao
# SCREEN_WIDTH = TILE_SIZE * WORLD_WIDTH
# SCREEN_HEIGHT = TILE_SIZE * WORLD_HEIGHT

class Orient(Enum):
    NONE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    TOPLEFT_IN = 5
    TOPRIGHT_IN = 6
    BOTTOMLEFT_IN = 7
    BOTTOMRIGHT_IN = 8
    TOPLEFT_OUT = 9
    TOPRIGHT_OUT = 10
    BOTTOMLEFT_OUT = 11
    BOTTOMRIGHT_OUT = 12


class OrigOrient(Enum):
    NONE = 0
    HORIZONTAL = 3
    VERTICAL = 4
    TOPLEFT = 5
    TOPRIGHT = 6
    BOTTOMLEFT = 7
    BOTTOMRIGHT = 8
    CENTER = 9
    TOP_T = 10
    BOTTOM_T = 11
    LEFT_T = 12
    RIGHT_T = 13
    LEFT_END = 14
    RIGHT_END = 15
    TOP_END = 16
    BOTTOM_END = 17
    SURROUNDED = 18
