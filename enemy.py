import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image, type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 5)
        self.health = random.randint(5, 15)
        self.type = type

        if self.type == "tank":
            self.health = 100
            self.speed = 1


    def update(self):
        self.rect.x -= self.speed
        if self.rect.left <= 0:
            self.kill()