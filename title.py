import pygame

from config import *

from button import Button, AABB

T_INGAME = 1
T_INTITLE = 2

class Title:
    def __init__(self):
        self.ss = pygame.image.load("Assets Folder/chromophilia.png").convert()
        self.buttons = []
        tt = ['play', 'credits', 'settings']
        for i in range(3):
            self.buttons.append(Button(SCREEN_WIDTH / 2, 660 + i * 150, 300, 150, tt[i], i))
        self.ongame = False

    def process(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.buttons[0].has(x, y):
                self.ongame = True

    def draw(self, s):
        w, h = s.get_size()
        for i in range(3):
            self.buttons[i].aabb = AABB.c(w / 2, 660 + i * 150, 300, 150)
        if self.ongame:
            return False
        s.blit(self.ss, (0, 0))
        for b in self.buttons:
            b.draw(s)
        return True
