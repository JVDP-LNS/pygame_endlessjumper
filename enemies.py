import pygame
from random import randint

screen_x = 800


def get_fly():
    fly_surf = pygame.image.load("Sprites/enemy2.png").convert_alpha()
    fly_y = 200
    return fly_surf.get_rect(topleft=(screen_x + randint(100, 300), fly_y))
