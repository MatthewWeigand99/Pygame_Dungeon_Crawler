import pygame
import constants
from character import Character
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

# Game Clock
clock = pygame.time.Clock()

# Define player movement variables
move_left = False
move_right = False
move_up = False
move_down = False

# Scaling Helper Function
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    
    return pygame.transform.scale(image, (w * scale, h * scale))

# Load weapon images
bow_image = scale_img(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)

# Load character images
mob_animations = []
mob_types = ['elf', 'imp', 'skeleton', 'goblin', 'muddy', 'tiny_zombie', 'big_demon']

animation_types = ['idle', 'run']
for mob in mob_types:
    
    # Load images
    animation_list = []
    for ani in animation_types:
        # Temporary list
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f'assets/images/characters/{mob}/{ani}/{i}.png').convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)
    
# Create Player      
player = Character(100, 100, mob_animations, 0)

# Create player weapon
bow = Weapon(bow_image)

# Main Game Loop
run = True
while run:
    
    screen.fill(constants.BACKGROUND)
    
    # Player Movement Calculations
    dx = 0
    dy = 0
    
    if move_left:
        dx = -constants.SPEED
    if move_right:
        dx = constants.SPEED
    if move_up:
        dy = -constants.SPEED
    if move_down:
        dy = constants.SPEED
    
    player.move(dx, dy)
    
    # Update player
    player.update()
    bow.update(player)
    
    # Draw player on screen
    player.draw(screen)
    bow.draw(screen)
    
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