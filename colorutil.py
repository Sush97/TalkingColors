# Erik Ackermann
# Richard Boyle
# Kate Hansen
#
# SLP - Project 3
# Friday, April 20, 2012

# Colorutil module for color picker SDS
# Contains color object classes and a color window class

import sys
import pygame

class ColorState(object):
    """ Color state object
    """
    
    user_color = None
    window = None
    
    def init(self, r=255, g=255, b=255):
    
        pygame.init() 
    
        # define window parameters
        width = 400
        height = 400
        
        # create the screen
        self.window = pygame.display.set_mode((width, height))
        
        # fill it with starting color
        start_color = pygame.Color(r, g, b, 100)
        self.window.fill(start_color)
        
        #draw it to the screen
        pygame.display.flip()
        
    
    def update(self, newColor):
        """ newColor is a pygame.Color() object
        """
        
        self.user_color = newColor
        self.window.fill(newColor)
        pygame.display.flip()
    
    def getRGB(self):
        """ Returns tuple of <R, G, B> values
        """
        
        return str(self.user_color.r) + " " + str(self.user_color.g) + \
            " " + str(self.user_color.b)
    
    def getHEX(self):
        """ Returns a string representing the Hex value of the user color
        """
        
        return
                