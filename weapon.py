import pygame
import math
import random
import constants

class Weapon():
    def __init__(self, image, arrow_image):
        self.org_image = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect()
        self.arrow_image = arrow_image
        self.fired = False
        self.last_shot = pygame.time.get_ticks()
        
    def update(self, player):
        shot_cooldown = 300
        arrow = None
        
        self.rect.center = player.rect.center
        
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery) # Negative because pygame y coordinate increases downwards
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        
        # Get mouse click
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown:
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
        
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
            
        return arrow
    
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))
        
class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.org_image = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.org_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Calculate the orizontal and vertical speeds based on angle
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED)
        
    def update(self,screen_scroll, enemy_list):
        
        # Reset damage
        damage = 0
        damage_pos = None
        
        # Reposition based on speed
        self.rect.x += screen_scroll[0] + self.dx
        self.rect.y += screen_scroll[1] + self.dy
        
        # Check if arrow is off screen
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill()
            
        # Check enemy collision
        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect) and enemy.alive:
                damage = 10 + random.randint(-5, 5)
                damage_pos = enemy.rect
                enemy.health -= damage
                self.kill()
                break
        
        return damage, damage_pos
    
    def draw(self, surface):
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width() / 2)), self.rect.centery - int(self.image.get_height() / 2)))