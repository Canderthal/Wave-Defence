import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))

# Create two Rects (sprites)
sprite1 = pygame.Rect(100, 300, 50, 50)
sprite2 = pygame.Rect(600, 300, 50, 50)

# Create a bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 5
        self.angle = angle

    def update(self):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

# Load your sprite image (replace 'sprite_image.png' with your image file)
sprite_image = pygame.image.load("assets/turret/turret_bullet.png")
sprite_rect = sprite_image.get_rect()

# Create a list to store bullets
bullets = []

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fire a bullet when the player clicks the mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = sprite1.center
            angle = math.atan2(sprite2.centery - y, sprite2.centerx - x)
            bullets.append(Bullet(x, y, angle))

    # Calculate the angle between the two Rects
    angle = math.atan2(sprite2.centery - sprite1.centery, sprite2.centerx - sprite1.centerx)
    
    # Convert the angle to degrees and rotate the sprite
    rotated_sprite = pygame.transform.rotate(sprite_image, math.degrees(angle))
    
    # Update the sprite's Rect to the new position (center)
    sprite_rect = rotated_sprite.get_rect(center=sprite_rect.center)
    
    # Clear the screen
    screen.fill((0, 0, 0))
    
    # Draw the rotated sprite
    screen.blit(rotated_sprite, sprite_rect.topleft)
    
    # Update and draw the bullets
    for bullet in bullets:
        bullet.update()
        pygame.draw.rect(screen, (255, 0, 0), bullet.rect)
    
    # Detect collisions between bullets and sprite2 (tracked rect)
    for bullet in bullets:
        if bullet.rect.colliderect(sprite2):
            bullets.remove(bullet)
    
    # Update the display
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
