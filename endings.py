import pygame

class Dead:
    def __init__(self):
        self.ss = pygame.image.load("Assets Folder/youdied.png").convert_alpha()
        self.buttons = [
        ]
        self.goto_title = False

    def process(self, e):
        if e.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.buttons[0].has(x, y):
                self.goto_title = True

    def draw(self, s):
        s.blit(self.ss, (0, 0))
        if self.goto_title:
            return True
