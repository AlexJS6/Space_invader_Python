import pygame
import os
import time
import random

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
BG = pygame.image.load(os.path.join('assets', 'background-black.png'))

#main that makes the game run
def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    def redraw_window():

    while run:
        clock.tick(FPS)

        for event in pygame.event.get(): #pygame events
            if event.type == pygame.QUIT: # other ex: KEYDOWN
                run = False

main()
