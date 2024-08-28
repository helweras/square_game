import pygame


class Obstacle:
    def __init__(self, coord: tuple, width_screen, height_screen, size: tuple, color=(25, 255, 0)):
        self.params_screen = (width_screen, height_screen)
        self.image = pygame.Surface(size)  # это объект, представляющий собой поверхность для рисования.
        # Он используется для создания изображений, на которых можно рисовать графику, текст и другие элементы.

        self.image.fill(color)  # Заполнение объекта цветом
        self.rect = self.image.get_rect()
        self.rect.topleft = coord  # Задание координат левого верхнего угла
        self.old_position = self.rect.topleft
        self.color = color
        self.size = size

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


class Bonus(Obstacle):
    def __init__(self, coord: tuple, width_screen, height_screen, size: tuple, color):
        super().__init__(coord, width_screen, height_screen, size, color)


class CircleObject:
    def __init__(self, radius):
        # Создаем поверхность с учетом размера круга и добавляем флаг SRCALPHA для прозрачности
        self.surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.radius = radius
        self.rect = self.surface.get_rect()

        # Рисуем круг на этой поверхности
        pygame.draw.circle(self.surface, (255, 0, 0), (radius, radius), radius)

    def draw(self, target_surface):
        # Отображаем круг на целевой поверхности
        target_surface.blit(self.surface, self.rect.center)