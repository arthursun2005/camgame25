import pygame

from config import *


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game:
    def __init__(self):
        self.in_dialogue = False
        try:
            pygame.mixer.init()
            self.music = pygame.mixer.Sound("assets/music/m.wav")
            self.music.play(-1)
        except:
            pass
