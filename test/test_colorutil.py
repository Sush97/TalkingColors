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

x = 0

while x < 240:
    
    x += 10
    a = raw_input()
    green = pygame.Color(0, x, 0, 100)
    if x < 20:
        myState.updateWithString('purple')
    elif x < 60:
        myState.changeAttribute('brightness', 'much', 'less')
    elif x < 230:
        myState.changeAttribute('saturation', 'a little', 'less')
    else:
        myState.updateWithColor(green)


print("Your color is " + myState.getRGB())