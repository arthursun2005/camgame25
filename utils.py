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

def collision(a: pygame.rect.Rect, b: pygame.rect.Rect):
    colls = set()
    h = min(a.bottom, b.bottom) - max(a.top, b.top)
    w = min(a.right, b.right) - max(a.left, b.left)
    if w <= 0 or h <= 0:
        colls.add(Collision.NONE)
        return colls
    if b.top < a.top and b.bottom - a.top <= COLL_THRES:
        colls.add(Collision.TOP)
    if a.top < b.top and a.bottom - b.top <= COLL_THRES:
        colls.add(Collision.BOTTOM)
    if b.left < a.left and b.right - a.left <= COLL_THRES:
        colls.add(Collision.LEFT)
    if a.left < b.left and a.right - b.left <= COLL_THRES:
        colls.add(Collision.RIGHT)
    if not colls:
        colls.add(Collision.NONE)
    return colls
