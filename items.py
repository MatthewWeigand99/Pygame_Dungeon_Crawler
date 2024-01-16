import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animation_list, dummy_coin = False):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0 is coin and 1 is a potion
        self.animation_list = animation_list
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.dummy_coin = dummy_coin

    def update(self,screen_scroll, player):
        if not self.dummy_coin:
            # Reposition based on screen scroll
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        
        # Check collection
        if self.rect.colliderect(player.rect):
            # Coin collected
            if self.item_type == 0:
                player.score += 1
            # Potion collected
            elif self.item_type == 1:
                player.health += 10
                if player.health > 100:
                    player.health = 100
            
            self.kill()
            
        # Handle animation
        ani_cooldown = 150
        # Update image
        self.image = self.animation_list[self.frame_index]
        # Check time since last update
        if pygame.time.get_ticks() - self.update_time > ani_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
    def draw(self, surface):
        surface.blit(self.image, self.rect)