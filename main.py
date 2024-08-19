import pygame
import sys
from character import MainPlayer
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
        self.WIDTH, self.HEIGHT = self.get_screen_info()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Collision Example")
        self.clock = pygame.time.Clock()

        self.RED = (255, 0, 0)

        self.player = MainPlayer((220, 10), self.WIDTH, self.HEIGHT, color=self.RED, size=(50, 50))
        self.base = None

        self.obstacle = []
        self.bonus = obj.Bonus((400, 150), self.WIDTH, self.HEIGHT, size=(30, 30), color=(0, 0, 0))
        self.play_map = None

    @staticmethod
    def get_screen_info():
        """Получение параметров экрана.
        Вовращает размеры экрана в пикселях"""
        info = pygame.display.Info()
        return info.current_w, info.current_h

    @staticmethod
    def spawn(card: list, size: tuple, h, w):
        """Размещает на матрице объекты.
        1 = пиксель объекта, 0 = отсутствие пикселя объекта на экране и матрице"""
        for y in range(h, h + size[1]):
            for x in range(w, w + size[0]):
                card[y][x] = 1

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

    def control_spawn_obstacle(self, count: int, pl_map: list, right, down):
        """Контролирует появление объектов типа Obstacle на экране согласно их колличеству count и добавляет объекты
        в self.obstacle"""
        flag = 0
        w = random.randint(50, self.WIDTH - 150)
        h = random.randint(50, self.HEIGHT - 100)
        while flag < count:
            if pl_map[h][w] == 0:
                self.obstacle.append(obj.Obstacle((w, h), self.WIDTH, self.HEIGHT, size=(140, 40)))
                self.spawn(pl_map, (150, 20), h, w)
                flag += 1
                w = random.randint(50, self.WIDTH - 150)
                h = random.randint(50, self.HEIGHT - 100)
            else:
                w = random.randint(50, self.WIDTH - 150)
                h = random.randint(50, self.HEIGHT - 100)

    def gen_play_map(self):
        """Генерация матрицы карты.
        Возвращает List() и self.play_map = play_map"""
        play_map = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.play_map = play_map
        return play_map

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

    def control_spawn_base(self, game_map: list):
        """Проверяет условия появления базы и добавляет объект типа Base в атрибут self.base"""
        for h in range(50, len(game_map) - 50):
            for x in range(50, len(game_map[h]) - 50):
                pass

    # def prerun(self):
    #     self.control_spawn_obstacle(10, self.gen_play_map(), self.WIDTH, self.HEIGHT)

    def run(self):
        self.control_spawn_obstacle(4, self.gen_play_map(), self.WIDTH, self.HEIGHT)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # self.player.update_position()
            self.constant_movement(self.player)
            # Проверка столкновений с препятствием и границами экрана
            self.player.stop_screen()
            self.check_collision_obstacle(self.player)

            font = pygame.font.Font(None, 25)
            text = font.render(self.name_color_background, True, (0, 0, 0))
            text_rect = text.get_rect(center=(300, 300))

            if self.player.rect.colliderect(self.bonus.rect):
                self.new_color_background()
                font = pygame.font.Font(None, 25)
                text = font.render(self.name_color_background, True, (0, 0, 0))
                text_rect = text.get_rect(center=(300, 300))
                if self.bonus.rect.right - self.WIDTH > -30:
                    self.bonus.move(-self.WIDTH + 120, 0)
                else:
                    self.bonus.move(50, 0)

            self.screen.fill(self.code_color_background)
            self.screen.blit(text, text_rect)
            self.player.draw(self.screen)
            for i in self.obstacle:
                i.draw(self.screen)
            self.bonus.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
