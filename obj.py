import pygame


class Obstacle:
    def __init__(self, coord, size, color=None):
        self.obstacle_surface = pygame.Surface(size, pygame.SRCALPHA)
        self.obs_image = pygame.image.load('obstacle_gate.png').convert_alpha()
        self.obs_image = pygame.transform.scale(self.obs_image, size)
        self.obstacle_surface.blit(self.obs_image, (0, 0))
        self.obstacle_rect = self.obstacle_surface.get_rect(topleft=coord)
        self.obstacle_mask = pygame.mask.from_surface(self.obstacle_surface)

    def draw_in_screen(self, screen):
        screen.blit(self.obstacle_surface, self.obstacle_rect)

    # def reset_position(self):
    #     self.rect.topleft = self.old_position
    #
    # def move(self, x, y):
    #     self.old_position = self.rect.topleft
    #     self.rect.x += x
    #     self.rect.y += y

    # def stop_screen(self):
    #     if self.rect.left < 0:
    #         self.rect.left = 0
    #     if self.rect.right > self.params_screen[0]:
    #         self.rect.right = self.params_screen[0]
    #     if self.rect.top < 0:
    #         self.rect.top = 0
    #     if self.rect.bottom > self.params_screen[1]:
    #         self.rect.bottom = self.params_screen[1]


class Bonus(Obstacle):
    def __init__(self, coord: tuple, size: tuple, color):
        super().__init__(coord, size, color)


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
