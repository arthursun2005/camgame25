import pygame

class Dead:
    def __init__(self):
        self.ss = pygame.image.load("Assets Folder/youdied.png").convert_alpha()

    def draw(self, s):
        s.blit(self.ss, (0, 0))
