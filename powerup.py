import pygame


class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 1

    def update(self):
        self.rect.x -= self.speed
        if self.rect.left <= 0:
            self.kill()