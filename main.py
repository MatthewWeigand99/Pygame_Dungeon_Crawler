import pygame
import csv
import constants
from world import World
from character import Character
from weapon import Weapon
from items import Item

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption('Dungeon Crawler')

# Game Clock
clock = pygame.time.Clock()

# Define game variables
level = 1

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

# Load coin images
coin_img_list = []
for x in range(4):
    img = scale_img(pygame.image.load(f'assets/images/items/coin_f{x}.png').convert_alpha(), constants.ITEM_SCALE)
    coin_img_list.append(img)
    
# Load tile map images
tile_list =[]
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f'assets/images/tiles/{x}.png').convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

# Load potion image
potion_img = scale_img(pygame.image.load(f'assets/images/items/potion_red.png').convert_alpha(), constants.POTION_SCALE)

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

# Function to draw text to screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

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
    # Display score
    draw_text(f'X{player.score}', font, constants.WHITE, constants.SCREEN_WIDTH - 50, 15)

# Create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
# Load in level data and create world
with open(f'levels/level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list)

# Draw grid
#def draw_grid():
   #for x in range(30):
        #pygame.draw.line(screen, constants.WHITE, (x * constants.TILE_SIZE, 0), (x * constants.TILE_SIZE, constants.SCREEN_HEIGHT))
        #pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILE_SIZE), (constants.SCREEN_WIDTH, x * constants.TILE_SIZE))
    
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
item_group = pygame.sprite.Group()

score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_img_list)

potion = Item(200, 200, 1, [potion_img])
item_group.add(potion)
coin = Item(400, 400, 0, coin_img_list)
item_group.add(coin)

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
    item_group.update(player)
    
    # Draw on screen
    world.draw(screen)
    
    player.draw(screen)
    
    bow.draw(screen)
    for arrow in arrow_group:
        arrow.draw(screen)
    for enemy in enemy_list:
        enemy.draw(screen)
    
    damage_text_group.draw(screen)
    
    item_group.draw(screen)
    draw_info()
    score_coin.draw(screen)
    
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