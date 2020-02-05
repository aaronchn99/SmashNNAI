from gamedata import GameDataAPI as gd

import math as m
import numpy as np
import pygame
pygame.init()

''' Colour triples '''
WHITE = (255,255,255)
BLACK = (0,0,0)

''' Control constants '''
START_RES = (500,500)
IMG_SIZE = (60,50)
INVGAPSIZE = 14    # Inverse of player to opponent gap size (Low => Longer gap, High => Shorter gap)
