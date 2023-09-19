import pygame
import random
import constants
from enemy import Enemy
from powerup import Powerup
from turret import Turret
import math

#Player starts with cheap tank traps
#more money will unlock turrets


WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()


#######################___Window Information___#######################
screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Wave Survival")
######################################################################


#######################___Load images___#######################
background = pygame.image.load("assets/backgrounds/background.png")
turret_base = pygame.image.load("assets/turret/turret_base.png")
turret_top = pygame.image.load("assets/turret/turret_top.png")
turret_bullet = pygame.image.load("assets/turret/turret_bullet.png")
mob = pygame.image.load("mob.png")
mob_tank = pygame.image.load("power_up.png")
###############################################################

#######################___Load sound___#######################
shot_sound = pygame.mixer.Sound("turret_shot.wav")



#######################___Sprite Groups___#######################
powerup_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
turret_list = pygame.sprite.Group()
turret_guns = pygame.sprite.Group()
sprite_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
###############################################################
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class Bullet:
    def __init__(self, x, y, angle):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 5
        self.angle = angle

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

def spawn_turret():
    pos = pygame.mouse.get_pos()
    x_pos = pos[0]
    y_pos = pos[1]
    turret = Turret(x_pos, y_pos, 25, 25, turret_base, turret_top, turret_bullet)
    turret_list.add(turret)
    sprite_list.add(turret)


def spawn_enemy(amount):
    for _ in range(amount):
        x = random.randint(1,10)
        if x == 10:
            image = mob_tank
            mob_type = "tank"
        else:
            image = mob       
            mob_type = "normal"
        enemy = Enemy(WIDTH + random.randint(10, 100), random.randint(50, HEIGHT - 50), 10, 10, image, mob_type) 
        enemy_list.add(enemy)
        sprite_list.add(enemy)

def move_enemy():
    for enemy in enemy_list:
        enemy.update()
        enemy_list.draw(screen)
        if enemy.rect.left <= 0:
            enemy_list.remove(enemy)
            spawn_enemy(1)

def powerup(amount):
    for _ in range(amount):
        power = Powerup(WIDTH + random.randint(10, 200), random.randint(50, HEIGHT - 50), 20, 20, power_up_image)
        powerup_list.add(power)
def move_powerup():
    for power in powerup_list:
        power.update()
        powerup_list.draw(screen)
        if power.rect.left <= 0:
            powerup_list.remove(power)

def display_target_priority_menu(turret):
    menu_font = pygame.font.Font(None, 36)
    text = ["Select Target Priority:", "1 - Closest Enemy", "2 - Strongest Enemy", "3 - Weakest Enemy"]
    text_y = turret.rect.centery + turret.rect.size[1] + 20

    for line in text:
        text_surface = menu_font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(constants.WIDTH // 2, text_y))
        screen.blit(text_surface, text_rect)
        text_y += 40


spawn_enemy(1)
#powerup(5)
money = 300
last_turret = pygame.time.get_ticks()
run = True
while run:
    clock.tick(FPS)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    move_enemy()
    for turret in turret_list:
        x = turret.target_enemy(enemy_list)
        turret.update(shot_sound)
        turret.draw(screen)
        turret.turret_bullets.update()
        for bullet in turret.turret_bullets:
            time = pygame.time.get_ticks()
            if time - bullet.fired_at > 400:
                turret.turret_bullets.remove(bullet)
            for enemy in enemy_list:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.health -= 10
                    if enemy.health <= 0:
                        enemy_list.remove(enemy)
                        if enemy.type == "tank":
                            money += 5
                        else:
                            money += 1
                    turret.turret_bullets.remove(bullet)
                    if len(enemy_list) < 5:
                        spawn_enemy(1)


        #Event Handler
    keys = pygame.key.get_pressed()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 2:
            if pygame.time.get_ticks() - last_turret >= 500 and money > 200:
                spawn_turret()
                money -= 200
                last_turret = pygame.time.get_ticks()
        elif event.button == 3:
            for turret in turret_list:
                if turret.rect.collidepoint(pygame.mouse.get_pos()):
                    display_target_priority_menu(turret)
                    pygame.display.flip()
                    waiting_for_input = True

                    while waiting_for_input:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1:
                                    turret.target_priority = "Closest Enemy"
                                elif event.key == pygame.K_2:
                                    turret.target_priority = "Strongest Enemy"
                                elif event.key == pygame.K_3:
                                    turret.target_priority ="Weakest Enemy"
                                waiting_for_input = False
    pygame.display.update()
    money += 0.5
    print(f"money: {money}")
pygame.quit()





#Need some sort of indication the type of target priority for turrets
#Diff pixel image if strongest. Green, yellow, red ?