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
    
    preset_color_values = {'red': (255, 0, 0),
                        'orange': (255, 165, 0),
                        'yellow': (255, 255, 0),
                        'green': (0, 120, 0),
                        'blue': (0, 0, 255),
                        'purple': (160, 32, 240),
                        'black': (0, 0, 0),
                        'white': (255, 255, 255),
                        'pink': (255, 192, 203),
                        'grey': (190, 190, 190),
                        'gray': (190, 190, 190)}
    
    preset_degree_values = {'a lot': 16,
                            'much': 8,
                            'a little': 4,
                            'a tiny bit': 2}
    
    preset_direction_values = {'more': 1, 'less': -1}
    
    def init(self, r=255, g=255, b=255):
    
        pygame.init() 
    
        # define window parameters
        width = 400
        height = 400
        
        # create the screen
        self.window = pygame.display.set_mode((width, height))
        
        # fill it with starting color
        self.user_color = pygame.Color(r, g, b)
        self.window.fill(self.user_color)
        
        #draw it to the screen
        pygame.display.flip()
        
    
    def updateWithColor(self, newColor):
        """ newColor is a pygame.Color() object
        """
        
        self.user_color = newColor
        self.window.fill(self.user_color)
        pygame.display.flip()
        
    def updateWithString(self, newColorString):
        """ Set the state with a color name string
            Accepted values are:
                red, orange, yellow, green, blue, purple, black, white, pick, grey
        """
        
        col = self.preset_color_values[newColorString.lower()]
        newColor = pygame.Color(col[0], col[1], col[2])
        self.user_color = newColor
        self.window.fill(self.user_color)
        pygame.display.flip()
    
    def changeBrightness(self, degree, direction):
        """ Change the brightness
            Degree is the amount of change
            Direction is either "more" for brighter or "less" for darker
        """
        
        sign = self.preset_direction_values[direction]
        brightness = self.user_color.hsva[2]
        brightness += self.preset_degree_values[degree]*sign
        self.user_color.hsva = (self.user_color.hsva[0],
                            self.user_color.hsva[1],
                            max(min(brightness, 100), 0),
                            self.user_color.hsva[3])
        self.window.fill(self.user_color)
        pygame.display.flip()
        
    def changeSaturation(self, degree, direction):
        """ Change the saturation
            Degree is the amount of change
            Direction is either "more" for more saturated or "less" for less saturated
        """
        
        sign = self.preset_direction_values[direction]
        saturation = self.user_color.hsva[1]
        saturation += self.preset_degree_values[degree]*sign
        self.user_color.hsva = (self.user_color.hsva[0],
                            max(min(saturation, 100), 0),
                            self.user_color.hsva[2],
                            self.user_color.hsva[3])
        self.window.fill(self.user_color)
        pygame.display.flip()
    
    def getRGB(self):
        """ Returns string of the (R, G, B) value of the user color
        """
        
        return str(self.user_color.r) + " " + str(self.user_color.g) + \
            " " + str(self.user_color.b)
    
    def getHEX(self):
        """ Returns a string representing the Hex value of the user color
        """
        
        return
                