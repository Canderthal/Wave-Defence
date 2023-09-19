import pygame
import math
import constants
pygame.mixer.init()
class Turret(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, turret_base_image, turret_top_image, turret_bullet_image):
        super().__init__()
        self.turret_base_image = turret_base_image
        self.turret_top_image = turret_top_image
        self.rect = self.turret_base_image.get_rect()
        self.rect.center = (x, y)
        self.angle = 0
        self.target = None
        self.range = 100
        self.original_turret_image = turret_top_image
        self.last_shot = pygame.time.get_ticks()
        self.shot_cooldown = 500
        self.shortest_distance = 999
        self.turret_bullet_image = turret_bullet_image  # Add the turret bullet image
        self.turret_bullets = pygame.sprite.Group()  # Initialize a sprite group for turret bullets
        self.target_priority = "Closest Enemy"
        self.target_health = 10



    def update(self, sound):
        self.rotate_top_image()
        turret_angle = self.rotate_top_image()
        self.shoot(turret_angle, sound)
        self.target_health = 10

    def draw(self, screen):
        base_rect = self.turret_base_image.get_rect(center=self.rect.center)
        top_rect = self.turret_top_image.get_rect(center=self.rect.center)

        screen.blit(self.turret_base_image, base_rect.topleft)
        screen.blit(self.turret_top_image, top_rect.topleft)

        # Draw turret bullets
        self.turret_bullets.draw(screen)

    def target_enemy(self, enemy_list):
        self.angle = 0
        self.target = None
        shortest_distance = 500
        if self.target_priority == "Closest Enemy":
            for enemy in enemy_list:
                distance = math.sqrt((self.rect.centerx - enemy.rect.centerx) ** 2 + (self.rect.centery - enemy.rect.centery) ** 2)
                if distance < shortest_distance:
                    shortest_distance = distance
                    self.target = enemy
        elif self.target_priority == "Strongest Enemy":
            for enemy in enemy_list:
                if enemy.health >= self.target_health:
                    self.target_health = enemy.health
                    self.target = enemy
        elif self.target_priority == "Weakest Enemy":
            for enemy in enemy_list:
                if enemy.health < self.target_health:
                    self.target_health = enemy.health
                    self.target = enemy
                    self.target_health = 10

        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))
            return angle

    def rotate_top_image(self):
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            x = math.degrees(math.atan2(dy, dx))
            self.angle = math.degrees(math.atan2(dy, dx))
            self.turret_top_image = pygame.transform.rotate(self.original_turret_image, (-self.angle - 90))
            return x

    def shoot(self, turret_angle, sound):
        if pygame.time.get_ticks() - self.last_shot >= self.shot_cooldown:
            if self.target:
                x, y = self.rect.center
                target_x, target_y = self.target.rect.center
                angle = math.atan2(target_y - y, target_x - x) #+ math.radians(self.angle)#new after the + sign

                # Pass the angle to the bullets
                turret_bullet = TurretBullet(x, y, angle, turret_angle, self.turret_bullet_image)
                self.turret_bullets.add(turret_bullet)
                sound.set_volume(0.1)
                sound.play()

                self.last_shot = pygame.time.get_ticks()
                self.target = None
    
    




class TurretBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, turret_angle, image):
        super().__init__()
        self.original_image = image
        self.image = pygame.transform.rotate(self.original_image, -turret_angle - 90)              #math.degrees(angle) - 90)  # Rotate the bullet image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 20
        self.angle = angle
        self.fired_at = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)



#delete bullet after x distance to save memory
#firing multiple bullets for some reason