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

class = Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    


#main that makes the game run
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont('comicsans', 50)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0)) # blit takes an image and draws it to the window at the location indicated
        
        # draw text
        lives_label = main_font.render(f'Lives: {lives}', 1, (255, 255, 255)) #1 = antialising
        level_label = main_font.render(f'Level: {level}', 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() -10, 10)) # Dynamic fashion goes with all heights, widths

        pygame.display.update() # refresh the display, (redessine tout tout le temps)

    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get(): # pygame events
            if event.type == pygame.QUIT: # other ex: KEYDOWN
                run = False

main()
