import pygame
from character import MainPlayer
import obj
import sys
import pygame


def left(self, obst):
    return (obst.rect.right - self.rect.left) < (self.rect.bottom - obst.rect.top)


def right(self, obst):
    return self.rect.right - obst.rect.left < self.rect.bottom - obst.rect.top


def underarm_left(self, obst):
    return obst.rect.right - self.rect.left > obst.rect.bottom - self.rect.top


def underarm_right(self, obst):
    return self.rect.right - obst.rect.left > obst.rect.bottom - self.rect.top


def collision(self, obst):
    if self.rect.colliderect(obst):
        x, y = self.get_direction()
        # Коллизии с препятствием при прямом столкновении

        if x > 0 and y == 0:  # справа
            self.rect.right = obst.rect.left
        elif x < 0 and y == 0:  # слева
            self.rect.left = obst.rect.right
        elif y < 0 and x == 0:  # снизу
            self.rect.top = obst.rect.bottom
        elif y > 0 and x == 0:  # сверху
            self.rect.bottom = obst.rect.top

        # Коллизии с препятствием при диагональном соприкосновении

        elif (x < 0 and (y < 0 or y > 0)) and left(self, obst) and not underarm_left(self, obst):  # слева + верх и низ
            self.rect.left = obst.rect.right

        elif (x > 0 and (y < 0 or y > 0)) and right(self, obst) and not underarm_right(self, obst):  # справа + верх и низ
            self.rect.right = obst.rect.left

        elif (y < 0 and (x < 0 or x > 0)) and self.rect.bottom > obst.rect.bottom:
            self.rect.top = obst.rect.bottom

        elif (y > 0 and (x < 0 or x > 0)) and self.rect.top < obst.rect.top:
            self.rect.bottom = obst.rect.top
