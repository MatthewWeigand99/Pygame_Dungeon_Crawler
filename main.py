import pygame
import constants
from character import Character

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

# Game Clock
clock = pygame.time.Clock()

# Define player movement variables
move_left = False
move_right = False
move_up = False
move_down = False
speed = 5

# Create Player
player = Character(100, 100)

# Main Game Loop
run = True
while run:
    
    screen.fill(constants.BACKGROUND)
    
    # Player Movement Calculations
    dx = 0
    dy = 0
    if move_left:
        dx = -speed
    if move_right:
        dx = speed
    if move_up:
        dy = -speed
    if move_down:
        dy = speed
    
    player.move(dx, dy)
    
    # Draw player on screen
    player.draw(screen)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Key Pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True
        # Key Unpressed       
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_s:
                move_down = False

    #print(str(dx) + ", " + str(dy))

    pygame.display.update()
    # Framerate
    clock.tick(constants.FPS)
            
pygame.quit()