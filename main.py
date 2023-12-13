import pygame
import constants
from character import Character
from weapon import Weapon

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

# Game Clock
clock = pygame.time.Clock()

# Define font
font = pygame.font.Font('assets/fonts/AtariClassic.ttf', 20)

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

# Load heart images
heart_empty = scale_img(pygame.image.load('assets/images/items/heart_empty.png').convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load('assets/images/items/heart_half.png').convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load('assets/images/items/heart_full.png').convert_alpha(), constants.ITEM_SCALE)

# Load weapon images
bow_image = scale_img(pygame.image.load('assets/images/weapons/bow.png').convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load('assets/images/weapons/arrow.png').convert_alpha(), constants.WEAPON_SCALE)

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

# Function for displaying game information
def draw_info():
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    
    half_heart_drawn = False
    # Draw lives
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))
#Damage Text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Move damage text up
        self.rect.y -= 1
        
        # Delete counter after a few seconnds
        self.counter += 1
        if self.counter > 40:
            self.kill()
          
# Create Player      
player = Character(100, 100, 100, mob_animations, 0)

# Create enemy
enemy = Character(200, 300, 100, mob_animations, 1)

# Create player weapon
bow = Weapon(bow_image, arrow_image)

# Create empty enemy list
enemy_list = []
enemy_list.append(enemy)

# Create Sprite groups
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()

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
    
    # Updates
    player.update()
    
    for enemy in enemy_list:
        enemy.update()
    
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, damage_pos = arrow.update(enemy_list)
        if damage:
            damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
            damage_text_group.add(damage_text)
    damage_text_group.update()
    
    # Draw on screen
    player.draw(screen)
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    
    damage_text_group.draw(screen)
    draw_info()
    
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