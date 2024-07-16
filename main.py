import pygame
import sys
from character import MainPlayer
import obj
import game_situation as gs
from Color import color_random
from random import choice


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

        self.obstacle = [obj.Obj((201, 100 + 100 * i), self.WIDTH, self.HEIGHT, (100, 30)) for i in range(2)]
        self.bonus = obj.Bonus((400, 150), self.WIDTH, self.HEIGHT, size=(30, 30), color=(0, 0, 0))

    @staticmethod
    def get_screen_info():
        info = pygame.display.Info()
        return info.current_w, info.current_h

    def new_color_background(self):
        code_color, name_color = choice(list(color_random.get_colors().items()))
        self.name_color_background = name_color
        self.code_color_background = code_color
        self.screen.fill(code_color)

    def run(self):
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
                self.bonus.move(self.WIDTH, 0)

            self.screen.fill(self.code_color_background)
            self.screen.blit(text, text_rect)
            for i in self.obstacle:
                i.draw(self.screen)
            self.player.draw(self.screen)
            self.bonus.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
