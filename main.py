import pygame
import constants
from character import Character

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Create Player
player = Character(100, 100)

# Main Game Loop
run = True
while run:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Draw player on screen
    player.draw(screen)
    
    pygame.display.update()
            
pygame.quit()