import pygame

class AABB:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def has(self, x, y):
        return self.min_x < x < self.max_x and self.min_y < y < self.max_y

    def x(self):
        return (self.min_x + self.max_x) * 0.5

    def y(self):
        return (self.min_y + self.max_y) * 0.5

CC = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
]

class Button:
    def __init__(self, x, y, w, h, text, c):
        self.aabb = AABB(x - w/2, x + w/2, y - h/2, y + h/2)
        self.ss = pygame.image.load("Assets Folder/bar.png").convert_alpha()
        font = pygame.font.Font('Assets Folder/font.ttf', 96)
        self.image = font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(self.aabb.x(), self.aabb.y()))

        r, g, b = CC[c]
        w, h = self.ss.get_size()
        for i in range(h):
            for j in range(w):
                rr, gg, bb, aa = self.ss.get_at((j, i))
                self.ss.set_at((j, i), (rr * r, gg * g, bb * b, aa))

    def draw(self, s):
        r = self.ss.get_rect(center=(self.aabb.x(), self.aabb.y()))
        s.blit(self.ss, r)

        img = self.image
        x, y = pygame.mouse.get_pos()
        if self.has(x, y):
            img = pygame.transform.scale_by(img, 1.2)
        self.rect = img.get_rect(center=(self.aabb.x(), self.aabb.y()))
        s.blit(img, self.rect)

    def has(self, x, y):
        return self.aabb.has(x, y)
