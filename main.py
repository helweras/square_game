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
        self.code_color_background = '#2E8B57'
        self.WIDTH, self.HEIGHT = self.get_screen_size(1000, 700)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Collision Example")
        self.clock = pygame.time.Clock()
        self.fps = 20

        self.RED = (255, 0, 0)

        self.player = None
        self.base = None

        self.obstacle = []
        self.bonus = None
        self.play_map = None
        self.enemy_list = []

        self.obst1 = None

    @staticmethod
    def get_screen_size(size_x=0, size_y=0):
        """Получение параметров экрана.
        Вовращает размеры экрана в пикселях"""
        if size_x and size_y:
            return size_x, size_y
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
                # self.obstacle.append(obj.Obstacle((w, h), size=size_obstacle))
                self.spawn(pl_map, size_obstacle, h, w, 1)
                self.obst1 = obj.Obstacle((w, h), (100, 100))
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

    def spawn_player(self, size: tuple, color: tuple):
        x_size, y_size = size
        create = False
        w = random.randrange(0, self.WIDTH + 1 - x_size)
        h = random.randrange(0, self.HEIGHT + 1 - y_size)
        while not create:
            if self.check_area(size, w, h):
                self.player = MainPlayer(coord=(w, h), width_screen=self.WIDTH, height_screen=self.HEIGHT, size=size,
                                         color=color)
                self.spawn(self.play_map, size, h, w, 2)
                create = True
            else:
                w = random.randrange(0, self.WIDTH + 1 - x_size)
                h = random.randrange(0, self.HEIGHT + 1 - y_size)

    def spawn_bonus(self, size: tuple, color: tuple):
        x_size, y_size = size
        create = False
        w = random.randrange(0, self.WIDTH + 1 - x_size)
        h = random.randrange(0, self.HEIGHT + 1 - y_size)
        while not create:
            if self.check_area(size, w, h):
                self.bonus = obj.Bonus(coord=(w, h), size=size,
                                       color=color)
                self.spawn(self.play_map, size, h, w, 2)
                create = True
            else:
                w = random.randrange(0, self.WIDTH + 1 - x_size)
                h = random.randrange(0, self.HEIGHT + 1 - y_size)

    def check_collision(self, obst, player: MainPlayer):
        # Расчет смещения (offset) для проверки столкновения
        offset = (obst.obstacle_rect.x - player.rect.x, obst.obstacle_rect.y - player.rect.y)

        # Проверка на пересечение масок
        collision_point = player.mask.overlap(obst.obstacle_mask, offset)

        if collision_point:
            print("Столкновение обнаружено в точке:", collision_point)
            print(player.rect.topleft)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.rect.x -= 4
        if keys[pygame.K_RIGHT]:
            self.player.rect.x += 4
        if keys[pygame.K_UP]:
            self.player.rect.y -= 4
        if keys[pygame.K_DOWN]:
            self.player.rect.y += 4

    # def prerun(self):
    #     self.control_spawn_obstacle(10, self.gen_play_map(), self.WIDTH, self.HEIGHT)

    def run(self):
        dt = self.clock.tick(self.fps) / 1000
        self.control_spawn_obstacle(1, self.gen_play_map(), (0, self.WIDTH), (0, self.HEIGHT), (130, 70))
        self.spawn_player((300, 300), self.RED)
        # self.spawn_bonus(size=(30, 30), color=(234, 213, 110))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.player.update_position(dt)
            # self.constant_movement(self.player)
            # Проверка столкновений с препятствием и границами экрана
            self.check_collision(self.obst1, self.player)

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
            #         print(self.obstacle[0].rect.x)
            #         print(self.obstacle[0].rect.y)
            #         self.spawn_bonus(size=(30, 30), color=(234, 213, 110))

            self.screen.fill(self.code_color_background)
            self.screen.blit(text, text_rect)
            # self.player.animation(dt)
            self.player.draw_in_screen(self.screen)
            self.obst1.draw_in_screen(self.screen)
            # self.screen.blit(self.obst1.surface, self.obst1.rect.topleft)
            # for i in self.obstacle:
            #     i.draw_in_screen(self.screen)
            # self.bonus.draw_in_screen(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        # print(*self.play_map, sep='\n')
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
