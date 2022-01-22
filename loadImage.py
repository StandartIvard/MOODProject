import sys
import pygame
import os


def load_hand_image(name, colorkey=None):
    fullname = os.path.join('', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


def load_enemy_image(name, colorkey=None):
    fullname = os.path.join('', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image, image.get_rect().size