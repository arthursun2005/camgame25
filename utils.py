from config import *
import pygame
from pygame.math import Vector2

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

def line_intersect(p1, p2, p3, p4):
    o1 = Vector2(p1)
    d1 = Vector2(p2) - Vector2(p1)
    o2 = Vector2(p3)
    d2 = Vector2(p4) - Vector2(p3)
    
    det = d1.cross(d2)
    if abs(det) < 0.01:
        return None

    diff = o2 - o1
    s = diff.cross(d2) / det
    t = diff.cross(d1) / det

    if 0 <= s <= 1 and 0 <= t <= 1:
        intersection = o1 + s * d1
        return (intersection.x, intersection.y)

    return 

def distance(p1,p2):
    p1 = Vector2(p1)
    p2 = Vector2(p2)
    return (p1-p2).magnitude()