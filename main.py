import pygame
import sys
from character import MainPlayer
import obj
import game_situation as gs
from Color import color_random
from random import choice
import random
import generation_map


class Game:
    def __init__(self):
        pygame.init()
        self.name_color_background = 'Белый'
        self.code_color_background = '#FFFFFF'
        self.get_screen_info()
        self.WIDTH, self.HEIGHT = self.get_screen_info()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Collision Example")
        self.clock = pygame.time.Clock()

        self.RED = (255, 0, 0)

        self.player = MainPlayer((220, 10), self.WIDTH, self.HEIGHT, color=self.RED, size=(50, 50))

        self.obstacle = []
        self.obs = [obj.Obj((23, 33), 10, 10, (22, 33)) for i in range(5)]
        self.bonus = obj.Bonus((400, 150), self.WIDTH, self.HEIGHT, size=(30, 30), color=(0, 0, 0))

        self.play_map = None

    @staticmethod
    def get_screen_info():
        info = pygame.display.Info()
        return info.current_w, info.current_h

    @staticmethod
    def spawn(card: list, size: tuple, h, w):
        for y in range(h, h + size[1]):
            for x in range(w, w + size[0]):
                card[y][x] = 1

    def control_spawn(self, count: int, pl_map: list, right, down):
        flag = 0
        w = random.randint(50, self.WIDTH - 150)
        h = random.randint(50, self.HEIGHT - 20)
        while flag < count:
            if pl_map[h][w] == 0:
                self.obstacle.append(obj.Obj((w, h), self.WIDTH, self.HEIGHT, size=(150, 100)))
                self.spawn(pl_map, (150, 20), h, w)
                flag += 1
                w = random.randint(50, self.WIDTH - 150)
                h = random.randint(50, self.HEIGHT - 20)
            else:
                w = random.randint(50, self.WIDTH - 150)
                h = random.randint(50, self.HEIGHT - 20)

    def gen_play_map(self):
        play_map = [[0 for i in range(self.WIDTH)] for j in range(self.HEIGHT)]
        self.play_map = play_map
        return play_map

    def new_color_background(self):
        code_color, name_color = choice(list(color_random.get_colors().items()))
        self.name_color_background = name_color
        self.code_color_background = code_color
        self.screen.fill(code_color)

    def prerun(self):
        self.control_spawn(10, self.gen_play_map(), self.WIDTH, self.HEIGHT)

    def run(self):
        self.control_spawn(20, self.gen_play_map(), self.WIDTH, self.HEIGHT)
        print(self.obstacle)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.player.update_position()

            # Проверка столкновений с препятствием и границами экрана
            self.player.stop_screen()
            for i in self.obstacle:
                gs.collision(self.player, i)

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
                    print(self.bonus.rect.right, f'{self.WIDTH} = Width')

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
