import pygame
import os
import time
import random
pygame.font.init() # to write ex: score

# Game window
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# name display
pygame.display.set_caption('Space Shooter')

# Images
RED_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_red_small.png'))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_green_small.png'))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_blue_small.png'))
# Player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assets', 'pixel_ship_yellow.png'))

# Shooting
RED_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_red.png'))
GREEN_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_green.png'))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_blue.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assets', 'pixel_laser_yellow.png'))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'background-black.png')), (WIDTH, HEIGHT))

class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
    
    def get_width(self):
        return self.ship_img.get_width() # to get width

    def get_height(self):
        return self.ship_img.get_height() # getter -> height (get_width and get_height native)


class Player(Ship): # Inheriting Ship
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health) # super() calls whole Ship class -> __init__
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # mask is for collision (where pixels are)
        self.max_health = health

class Enemy(Ship):
    COLOR_MAP = {
        'red': (RED_SPACE_SHIP, RED_LASER),
        'green': (GREEN_SPACE_SHIP, GREEN_LASER),
        'blue': (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health = 100): # here added color because there are different
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color] # To get right ship (check dictionnary just above)
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


#main that makes the game run
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)

    enemies = [] # Stoe the enemies here
    wave_length = 5 # Every level new wave
    enemy_vel = 1

    player_vel = 5 # velocity relative to fps because the time you are pressed if more fps more accounted

    player = Player(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0)) # blit takes an image and draws it to the window at the location indicated
        
        # draw text
        lives_label = main_font.render(f'Lives: {lives}', 1, (255, 255, 255)) #1 = antialising
        level_label = main_font.render(f'Level: {level}', 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() -10, 10)) # Dynamic fashion goes with all heights, widths
 
        for enemy in enemies:
            enemy.draw(WIN) # Draw is inherited

        player.draw(WIN)

        pygame.display.update() # refresh the display, (redessine tout tout le temps)

    while run:
        clock.tick(FPS)

        if len(enemies) == 0: #when no enemies anymore next level, harder wave, ...
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(['red', 'blue', 'green'])) #spawn them and y is very big difference so it seems like spawning different time
                enemies.append(enemy) # added to the enemies list


        for event in pygame.event.get(): # pygame events
            if event.type == pygame.QUIT: # other ex: KEYDOWN but here only registers 1 key at a time so not define here
                run = False

        keys = pygame.key.get_pressed() # checks every 60times/s if something got pressed
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel # moves 1 px to the left
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up for all for the and is for the restriction not to live the window
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT: # down
            player.y += player_vel

        for enemy in enemies:
            enemy.move(enemy_vel)

        redraw_window()

main()
