import pygame
import sys
from character import MainPlayer, Enemy
import obj
import game_situation as gs
from Color import color_random
from random import choice
import random


class Game:
    """Основной класс программы"""

    def __init__(self):
        pygame.init()  # Инициация всех модулей, которые входят в состав Pygame
        self.name_color_background = 'Белый'
        self.code_color_background = '#FFFFFF'
        self.get_screen_info()
        self.WIDTH, self.HEIGHT = 20, 10
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Collision Example")
        self.clock = pygame.time.Clock()

        self.RED = (255, 0, 0)

        self.player = MainPlayer((220, 10), self.WIDTH, self.HEIGHT, color=self.RED, size=(50, 50))
        self.base = None

        self.obstacle = []
        self.bonus = obj.Bonus((400, 150), self.WIDTH, self.HEIGHT, size=(30, 30), color=(0, 0, 0))
        self.play_map = None
        self.enemy_list = []

    @staticmethod
    def get_screen_info():
        """Получение параметров экрана.
        Вовращает размеры экрана в пикселях"""
        info = pygame.display.Info()
        return info.current_w, info.current_h

    @staticmethod
    def spawn(card: list, size: tuple, height, width, symbol):
        """Размещает на матрице объекты.
        1 = пиксель объекта, 0 = отсутствие пикселя объекта на экране и матрице"""
        size_x, size_y = size
        for height_pix in range(height, height + size_y):
            for width_pix in range(width, width + size_x):
                card[height_pix][width_pix] = symbol

    @staticmethod
    def constant_movement(any_obj):
        """Описывает постоянное движение в объекта в определенную сторону.
        Объект предающийся в функцию должен иметь метод move() и атрибут main_direction"""
        any_obj.move()
        keys = pygame.key.get_pressed()  # Получение нажитя клавиши
        if keys[pygame.K_DOWN]:
            any_obj.main_direction = 0, 1
        elif keys[pygame.K_LEFT]:
            any_obj.main_direction = -1, 0
        elif keys[pygame.K_RIGHT]:
            any_obj.main_direction = 1, 0
        elif keys[pygame.K_UP]:
            any_obj.main_direction = 0, -1

    def control_spawn_obstacle(self, count: int, pl_map: list, limit_x: tuple, limit_y: tuple, size_obstacle: tuple,
                               indent_x_0=0,
                               indent_y_0=0,
                               indent_x_1=0,
                               indent_y_1=0):
        """Контролирует появление объектов типа Obstacle на экране согласно их колличеству count и добавляет объекты
        в self.obstacle
        count - колличество препятствий
        pl_map - игровая карта в виде двумерного списка
        limit_x, limit_y - кортежи с крайними значениями в виде [от х до х1] для оси X и оси Y
        indent_x_0, indent_y_0, indent_x_1, indent_y_1 - отступы от крайних значений для осей X и Y, 0 для первого, 1 для второго
        """
        flag = 0
        x_0, x_1 = limit_x
        y_0, y_1 = limit_y
        obstacle_x, obstacle_y = size_obstacle
        area_obstacle = obstacle_x * obstacle_y
        total_area_obstacle = area_obstacle * count
        # случайное число в пределах по колличеству пикселей в ширину и высоту минус indend - отступ
        w = random.randrange(x_0 - indent_x_0, x_1 + 1 - (indent_x_1 + obstacle_x))
        h = random.randrange(y_0 - indent_y_0, y_1 + 1 - (indent_y_1 + obstacle_y))
        while flag < count:
            if pl_map[h][w] == 0:
                self.obstacle.append(obj.Obstacle((w, h), self.WIDTH, self.HEIGHT, size=size_obstacle))
                self.spawn(pl_map, size_obstacle, h, w, 1)
                flag += 1
                w = random.randrange(x_0 - indent_x_0, x_1 + 1 - (indent_x_1 + obstacle_x))
                h = random.randrange(y_0 - indent_y_0, y_1 + 1 - (indent_y_1 + obstacle_y))
            else:
                w = random.randrange(x_0 - indent_x_0, x_1 + 1 - (indent_x_1 + obstacle_x))
                h = random.randrange(y_0 - indent_y_0, y_1 + 1 - (indent_y_1 + obstacle_y))

    def gen_play_map(self):
        """Генерация матрицы карты.
        Возвращает List() и self.play_map = play_map"""
        play_map = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.play_map = play_map
        return play_map

    def check_area(self, size, index_w, index_h):
        """Проверка свободного места на карте для создания объекта заданного размера.
        Возвращает False если места нет и True если оно есть"""
        size_x, size_y = size
        for height_pix in range(index_h, index_h + size_y):
            for width_pix in range(index_w, index_w + size_x):
                if self.play_map[height_pix][width_pix] != 0:
                    return False
        return True

    def new_color_background(self):
        """Изменяет цвет фона"""
        code_color, name_color = choice(list(color_random.get_colors().items()))
        self.name_color_background = name_color
        self.code_color_background = code_color
        self.screen.fill(code_color)

    def check_collision_obstacle(self, object_for_collision):
        """Проверка столкновений объектов с препятствиями"""
        for obstacle in self.obstacle:
            gs.collision(object_for_collision, obstacle)

    def spawn_enemy(self, enemy: Enemy, count: int):
        """Контроль появления врагов типа Enemy"""
        x = random.randint(30, self.WIDTH - 50)
        y = random.randint(30, self.HEIGHT - 50)
        pass

    def spawn_player(self, coord: tuple, size: tuple, color: tuple):
        pass

    def spawn_bonus(self, coord: tuple, size: tuple, color: tuple):
        pass

    # def prerun(self):
    #     self.control_spawn_obstacle(10, self.gen_play_map(), self.WIDTH, self.HEIGHT)

    def run(self):
        self.control_spawn_obstacle(2, self.gen_play_map(), (0, self.WIDTH), (0, self.HEIGHT), (20, 3))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # self.player.update_position()
            # self.constant_movement(self.player)
            # Проверка столкновений с препятствием и границами экрана
            # self.player.stop_screen()
            # self.check_collision_obstacle(self.player)

            font = pygame.font.Font(None, 25)
            text = font.render(self.name_color_background, True, (0, 0, 0))
            text_rect = text.get_rect(center=(300, 300))

            # if self.player.rect.colliderect(self.bonus.rect):
            #     self.new_color_background()
            #     font = pygame.font.Font(None, 25)
            #     text = font.render(self.name_color_background, True, (0, 0, 0))
            #     text_rect = text.get_rect(center=(300, 300))
            #     if self.bonus.rect.right - self.WIDTH > -30:
            #         self.bonus.move(-self.WIDTH + 120, 0)
            #     else:
            #         self.bonus.move(50, 0)

            self.screen.fill(self.code_color_background)
            self.screen.blit(text, text_rect)
            # self.player.draw(self.screen)
            for i in self.obstacle:
                i.draw(self.screen)
            self.bonus.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        print(*self.play_map, sep='\n')
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
