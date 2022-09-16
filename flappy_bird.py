# Infinite Game

import pygame
import random


def genPipes():
    addToHigh = True
    upperPipes = []
    lowerPipes = []
    for i in range(6):
        if addToHigh:
            upperPipes.append(
                pygame.Rect(
                    i * 150 + 300,
                    0,
                    random.randint(70, 90),
                    random.randint(200, 333),
                )
            )
            addToHigh = False
        else:
            height = random.randint(200, 333)
            lowerPipes.append(
                pygame.Rect(
                    i * 150 + 300, 700 - height, random.randint(70, 100), height
                )
            )
            addToHigh = True
    if random.random() < 0.45:
        [rect.move_ip(190, 0) for rect in upperPipes]
        [rect.move_ip(-90, 0) for rect in lowerPipes]
    return upperPipes + lowerPipes


class Bird:
    def __init__(self):
        self.rect = pygame.Rect(100, 340, 35, 35)
        self.jumped = False
        self.jumpSpeed = 0

    def jump(self):
        self.jumpSpeed = 15

    def update(self):
        self.rect.move_ip(2, 5)
        self.rect.move_ip(0, -self.jumpSpeed)
        self.jumpSpeed -= 2 if self.jumpSpeed >= 0 else 1

    def render(self, screen):
        pygame.draw.rect(screen, (255, 58, 32), self.rect)


class Game:
    def __init__(self):
        self.pipes = genPipes()

    def generate(self):
        self.pipes = genPipes()

    def render(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, (0, 0, 0), pipe)


class App:
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None
        pygame.init()
        self.bird = None
        self.game = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("Flappy")
        self.bird = Bird()
        self.game = Game()
        self.clock = pygame.time.Clock()
        self.running = True

    def update(self):
        if self.bird.rect.top < 0 or self.bird.rect.top > 665:
            self.running = False
        if self.bird.rect.left > 1185:
            self.bird.rect.update(pygame.Rect(-15, self.bird.rect.top, 35, 35))
            self.game.generate()
        if any(map(lambda pipe: pipe.colliderect(self.bird.rect), self.game.pipes)):
            self.running = False
        self.bird.update()
        self.events()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if keys[pygame.K_SPACE] or any(mouse):
            self.bird.jump()

    def render(self):
        self.screen.fill((239, 236, 202))
        self.game.render(self.screen)
        self.bird.render(self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def cleanUp(self):
        pass


if __name__ == "__main__":
    app = App()
    app.run()
