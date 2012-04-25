import sys

#import and init pygame
import pygame
pygame.init() 

# define window parameters
width = 400
height = 400

# create the screen
window = pygame.display.set_mode((width, height))

# fill it with starting color
red = pygame.Color(255, 0, 0, 100)
window.fill(red)

#draw it to the screen
pygame.display.flip()

newColor = pygame.Color(red[0], 0, 0, 0)

while True: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit(0)
        elif event.type == pygame.MOUSEMOTION:
            x = event.dict['pos'][0] / (width * 1.0)
            y = event.dict['pos'][1] / (height * 1.0)
            h = newColor.hsva[0]
            a = newColor.hsva[3]
            newColor.hsva = (h, y*100, x*100, a)
            window.fill(newColor)
            pygame.display.flip()
            