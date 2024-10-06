import pygame
from Color import color_random
from random import choice
import pathlib
import math


class MainPlayer:

    def __init__(self, width_screen, height_screen, size: tuple, color, coord=(100, 100)):
        self.params_screen = (width_screen, height_screen)
        if color:
            self.name_color = color
        else:
            self.name_color = (255, 0, 0)
        self.size = size
        self.current_image = 0  # Индекс текущего кадра анимации, начинает с 0
        self.list_image_statick = [pygame.image.load(img).convert_alpha() for img in
                                   self.get_list_name_file('player_image/statick')]
        self.list_image_move = [pygame.image.load(img).convert_alpha() for img in
                                self.get_list_name_file('player_image/move')]
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.image = pygame.transform.scale(self.list_image_statick[self.current_image], size)
        self.rect = self.surface.get_rect(topleft=coord)
        self.flip = False

        self.time_passed = 0  # Счётчик времени, который отслеживает время, прошедшее с момента последнего обновления кадра
        self.time_press_key = 0

        # self.download_player_image(size)
        self.draw_image()

        self.mask = pygame.mask.from_surface(self.surface)
        self.old_position = self.rect.topleft

        self.speed = 8
        self.animation_speed = 0.355 - 0.102 * math.log(self.speed)  # Скорость анимации
        self.main_direction = 1, 0
        self.old_direction_x, self.old_direction_y = self.speed, 0

        # Вызовы методов

    def animation(self, dt):
        self.time_passed += dt
        if self.time_passed >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.list_image_move)
            self.image = pygame.transform.scale(self.list_image_move[self.current_image], self.size)
            self.draw_image()
            self.mask = pygame.mask.from_surface(self.image)
            self.time_passed = 0

    @staticmethod
    def flip_image(image_list: list, x=True, y=False):
        """Функция для отзеркаливания каринок внутри списка"""
        for indx_img in range(len(image_list)):
            image_list[indx_img] = pygame.transform.flip(image_list[indx_img], x, y)

    @staticmethod
    def get_list_name_file(path) -> list:
        folder_path = pathlib.Path(path)
        return [f'{path}/{f.name}' for f in folder_path.iterdir() if f.is_file()]

    def reset_position(self):
        self.rect.topleft = self.old_position

    def change_color(self):
        code_color, name_color = choice(list(color_random.get_colors().items()))
        self.surface.fill(code_color)
        self.name_color = name_color

    def move(self):
        """Для постоянного движения"""
        self.old_position = self.rect.topleft
        self.rect.x += self.speed * self.main_direction[0]
        self.rect.y += self.speed * self.main_direction[1]

    def move_control(self, x, y):
        """Для движения по нажатию кнопки"""
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

    def control_flip_image(self, dt):
        """Функция для определения момента отзеркаливания картинки в зависимости от напрвления движения персонажа
        присваевает новое значение для old_direction"""
        if self.get_direction():
            direction_x, direction_y = self.get_direction()
            if direction_x != self.old_direction_x:  # Если новое напраление движения отличается от старого по оси x
                self.flip_image(self.list_image_statick, direction_x)
                self.flip_image(self.list_image_move, direction_x)
            self.animation(dt)
            if direction_x == 0:
                direction_x = self.old_direction_x
            if self.old_direction_y == 0:
                direction_y = self.old_direction_y
            self.old_direction_x, self.old_direction_y = direction_x, direction_y
        else:
            self.image = pygame.transform.scale(self.list_image_statick[0], self.size)

    def update_position(self, dt):
        self.time_press_key += dt
        self.old_position = self.rect.topleft  # Сохраняем старую позицию
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_control(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move_control(1, 0)
        if keys[pygame.K_UP]:
            self.move_control(0, -1)
        if keys[pygame.K_DOWN]:
            self.move_control(0, 1)
        self.control_flip_image(dt)

    def draw_circle(self, size):
        center = (size[0] / 2, size[1] / 2)
        pygame.draw.circle(self.surface, color=(3, 123, 124), center=center, radius=center[1])

    def draw_image(self):
        """Загружает картинку и рисует ее на Surface"""
        # self.download_player_image(size)
        self.surface.blit(self.image, (0, 0))

    def draw_in_screen(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def get_direction(self):
        """Функция для получения напрвления движения персонажа по оси x и y
        Возвращает False если движения не было"""
        dx = self.rect.topleft[0] - self.old_position[0]
        dy = self.rect.topleft[1] - self.old_position[1]
        if dx == 0 and dy == 0:
            return False
        return dx, dy

    # def download_player_image(self, size):
    #     self.list_image = [pygame.image.load(f'player_image/{image}').convert_alpha() for image in
    #                        self.get_list_name_file('player_image')]
    #     self.image = pygame.transform.scale(self.list_image[self.current_image], size)

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


class Enemy(MainPlayer):
    """Враги летящие на персонажа"""

    def __init__(self, coord: tuple, width_screen, height_screen, size: tuple, color):
        super().__init__(coord, width_screen, height_screen, size, color)
