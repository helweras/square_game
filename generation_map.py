import pygame
import sys


class Character:
    def __init__(self, width, height, x, y, images):
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.images = [pygame.image.load(img).convert_alpha() for img in images]
        print(self.images)
        self.current_image = 0
        self.image = pygame.transform.scale(self.images[self.current_image], (width, height))
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_speed = 0.3  # Скорость анимации
        self.time_passed = 0

    def update(self, dt):
        # Обновляем кадр анимации
        self.time_passed += dt
        if self.time_passed >= self.animation_speed:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = pygame.transform.scale(self.images[self.current_image], (self.rect.width, self.rect.height))
            self.mask = pygame.mask.from_surface(self.image)
            self.time_passed = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Character Animation')
        # Замените на свои изображения анимации
        self.character = Character(300, 300, 100, 100, ['player_image/pers.png',
                                                        'player_image/Изготовка к прыжку.png',
                                                        'player_image/Прыжок.png'])
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000  # Дельта времени для обновления анимации
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((255, 255, 255))
            self.character.update(dt)
            self.character.draw(self.screen)

            pygame.display.flip()


x = [1,2,3,4]
for i in x:
    i += 5
print(x)
