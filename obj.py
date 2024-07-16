import pygame


class Obj:
    def __init__(self, coord: tuple, width_screen, height_screen, size: tuple, color=(255, 255, 0)):
        self.params_screen = (width_screen, height_screen)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        self.old_position = self.rect.topleft
        self.color = color

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset_position(self):
        self.rect.topleft = self.old_position

    def move(self, x, y):
        self.old_position = self.rect.topleft
        self.rect.x += x
        self.rect.y += y

    def stop_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.params_screen[0]:
            self.rect.right = self.params_screen[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.params_screen[1]:
            self.rect.bottom = self.params_screen[1]


class Bonus(Obj):
    def __init__(self, coord: tuple, width_screen, height_screen, size: tuple, color):
        super().__init__(coord, width_screen, height_screen, size, color)

