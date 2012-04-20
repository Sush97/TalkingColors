# Erik Ackermann
# Richard Boyle
# Kate Hansen
#
# SLP - Project 3
# Friday, April 20, 2012

# Colorutil module for color picker SDS
# Contains color object classes and a color window class

import pygame
from colorutil import *

myState = ColorState()
myState.init()
pygame.init()

green = pygame.Color(0, 255, 0, 100)

while 1:
    a = raw_input()
    myState.update(green)