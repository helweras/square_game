import pygame
from Color import color_random
from random import choice


class MainPlayer:

    def __init__(self, coord: tuple, width_screen, height_screen, size: tuple, color):
        self.params_screen = (width_screen, height_screen)
        if color:
            self.name_color = color
        else:
            self.color = (255, 0, 0)
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = coord
        self.old_position = self.rect.topleft
        self.speed = 4

    def reset_position(self):
        self.rect.topleft = self.old_position

    def change_color(self):
        code_color, name_color = choice(list(color_random.get_colors().items()))
        self.image.fill(code_color)
        self.name_color = name_color

    def move(self, x, y):
        self.rect.x += self.speed * x
        self.rect.y += self.speed * y

    def stop_screen(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.params_screen[0]:
            self.rect.right = self.params_screen[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.params_screen[1]:
            self.rect.bottom = self.params_screen[1]

    def update_position(self):
        self.old_position = self.rect.topleft  # Сохраняем старую позицию
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
        if keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_direction(self):
        dx = self.rect.topleft[0] - self.old_position[0]
        dy = self.rect.topleft[1] - self.old_position[1]
        return dx, dy

    # def collision(self, obst):
    #     if self.rect.colliderect(obst):
    #         x, y = self.get_direction()
    #
    #         # Коллизии с препятствием при прямом столкновении
    #
    #         if x > 0 and y == 0:  # справа
    #             self.rect.right = obst.rect.left
    #         elif x < 0 and y == 0:  # слева
    #             self.rect.left = obst.rect.right
    #         elif y < 0 and x == 0:  # снизу
    #             self.rect.top = obst.rect.bottom
    #         elif y > 0 and x == 0:  # сверху
    #             self.rect.bottom = obst.rect.top
    #
    #         # Коллизии с препятствием при диагональном соприкосновении
    #
    #         elif (x < 0 and (y < 0 or y > 0)) and self.rect.right > obst.rect.right:  # слева + верх и низ
    #             print(1)
    #             if self.rect.left - obst.rect.right == -self.speed:
    #                 self.rect.left = obst.rect.right
    #
    #             else:
    #                 if y > 0 and self.rect.top < obst.rect.top:
    #                     self.rect.bottom = obst.rect.top
    #                 else:
    #                     self.rect.top = obst.rect.bottom
    #
    #         elif (x > 0 and (y < 0 or y > 0)) and self.rect.left < obst.rect.left:  # справа + верх и низ
    #             print(2)
    #             if self.rect.right - obst.rect.left == self.speed:
    #                 self.rect.right = obst.rect.left
    #             else:
    #                 if y > 0 and self.rect.top < obst.rect.top:
    #                     self.rect.bottom = obst.rect.top
    #                 else:
    #                     self.rect.top = obst.rect.bottom
    #
    #         elif (y < 0 and (x < 0 or x > 0)) and self.rect.bottom > obst.rect.bottom:
    #             print(3)
    #             self.rect.top = obst.rect.bottom
    #
    #         elif (y > 0 and (x < 0 or x > 0)) and self.rect.top < obst.rect.top:
    #             print(4)
    #             self.rect.bottom = obst.rect.top
