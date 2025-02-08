from config import *

import pygame


def get_image(file, x, y):
    sprite = pygame.Surface((TILE_DEPTH, TILE_DEPTH), pygame.SRCALPHA, 32).convert_alpha()
    sprite.blit(file, (0, 0), (x * TILE_DEPTH, y * TILE_DEPTH, TILE_DEPTH, TILE_DEPTH))
    sprite = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
    return sprite

def get_square(colour):
    sprite = pygame.Surface((TILE_DEPTH, TILE_DEPTH), pygame.SRCALPHA, 32).convert_alpha()
    sprite.fill(colour)
    sprite = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
    return sprite
