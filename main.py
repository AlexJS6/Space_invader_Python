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

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return self.y <= height and self.y >= 0

    def collision(self, obj):
        return collide(self, obj)


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

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(x, y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
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

    def collide(obj1, obj2):
        offset_x = obj2.x - obj1.x
        offset_y = obj2.y - obj1.y
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None # Give 2 mask if overlaps brings back a tuple


#main that makes the game run
def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)
    lost_font = pygame.font.SysFont('comicsans', 60)

    enemies = [] # Stoe the enemies here
    wave_length = 5 # Every level new wave
    enemy_vel = 1

    player_vel = 5 # velocity relative to fps because the time you are pressed if more fps more accounted

    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

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

        if lost:
            lost_label = lost_font.render('YOU LOST!!', 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350)) # Math to put it in the middle

        pygame.display.update() # refresh the display, (redessine tout tout le temps)

    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost: # It is saying if lost_counter > FPS * 3 (3 seconds) stop the game, else dont move anything (go back to while loop)
            if lost_count > FPS * 3: # 3 seconds
                run = False
            else:
                continue

        if len(enemies) == 0: #when no enemies anymore next level, harder wave, ...
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(['red', 'blue', 'green'])) #spawn them and y is very big difference so it seems like spawning different time
                enemies.append(enemy) # added to the enemies list


        for event in pygame.event.get(): # pygame events
            if event.type == pygame.QUIT: # otherdwas ex: KEYDOWN but here only registers 1 key at a time so not define here
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

        for enemy in enemies[:]: # [:] -> Copy of the list so not modify the list we are looping through
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)



main()
