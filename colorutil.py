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
import math

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
    
    preset_degree_values = {'a lot': 25,
                            'much': 16,
                            'a little': 8,
                            'a tiny bit': 4}
    
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
        
    def updateWithString(self, newColorName, newColorAttribute=None):
        """ Set the state with a color name string
            Accepted values are:
                red, orange, yellow, green, blue, purple, black, white, pick, grey, gray
        """
        
        if newColorName == None:
            return
        
        col = self.preset_color_values[newColorName.lower()]
        print("Here is col:")
        print(col)
        newColor = pygame.Color(col[0], col[1], col[2])
        
        h = max(min(newColor.hsva[0], 360), 0)
        s = max(min(newColor.hsva[1], 100), 0)
        v = max(min(newColor.hsva[2], 100), 0)
        a = max(min(newColor.hsva[3], 100), 0)
        
        # Apply attributes (modifiers)
        if newColorAttribute in ["BRIGHT", "LIGHT", "DARK"]:
            brightness = v
            if newColorAttribute in ["BRIGHT", "LIGHT"]:
                brightness += 30
            elif newColorAttribute == "DARK":
                brightness -= 30
            brightness = float(max(min(brightness, 100), 0))
            newColor.hsva = (h, s, brightness, a)
        
        if newColorAttribute in ["SATURATED", "DESATURATED"]:
            saturation = s
            if newColorAttribute == "SATURATED":
                saturation += 30
            elif newColorAttribute == "DESATURATED":
                saturation -= 30
            saturation = float(max(min(saturation, 100), 0))
            newColor.hsva = (h, saturation, v, a)
        
        self.user_color = newColor
        self.window.fill(self.user_color)
        pygame.display.flip()
    
    def changeAttribute(self, attribute, degree, direction):
        """ Change the given attribute
            Degree is the amount of change
            Direction is either "more" for brighter or "less" for darker
        """
            
        if degree != None:    
            degree = degree.lower()
        # if no degree is specified, defaults to a little
        else:
            degree = "a little"
        
        if direction != None:
            direction = direction.lower()
        # if no degree is specified, defaults to more
        else:
            direction = "more"
        
        if attribute != None:
            attribute = attribute.lower()
            if attribute.upper() in ["BRIGHTER", "LIGHTER", "LIGHT", "BRIGHT"]:
                attribute = "brightness"
            elif attribute == "saturated":
                attribute = "saturation"
            elif attribute.upper() in ["DARKER", "DARK"]:
                attribute = "brightness"
                # and switch the direction
                if direction == "more":
                    direction = "less"
                else:
                    direction = "more"
            elif attribute == "desaturated":
                attribute = "saturation"
                # and switch the direction
                if direction == "more":
                    direction = "less"
                else:
                    direction = "more"
        else:
            return # attribute is required
        
        sign = self.preset_direction_values[direction]
        saturation = self.user_color.hsva[1]
        brightness = self.user_color.hsva[2]
        if attribute == "brightness":
            brightness += self.preset_degree_values[degree]*sign
            brightness = float(max(min(brightness, 100), 0))
            self.user_color.hsva = (max(min(self.user_color.hsva[0], 360), 0),
                                max(min(self.user_color.hsva[1], 100), 0),
                                brightness,
                                max(min(self.user_color.hsva[3], 100), 0))
        if attribute == "saturation":
            saturation += self.preset_degree_values[degree]*sign
            saturation = float(max(min(saturation, 100), 0))
            self.user_color.hsva = (max(min(self.user_color.hsva[0], 360), 0),
                                saturation,
                                max(min(self.user_color.hsva[2], 100), 0),
                                max(min(self.user_color.hsva[3], 100), 0))
        self.window.fill(self.user_color)
        pygame.display.flip()
    
    def adjustColor(self, color, degree, direction):
        """ Add more (or less) of a given color
            Degree is the amount of change
            Direction is either "more" for brighter or "less" for darker
        """
            
        if degree != None:    
            degree = degree.lower()
        # if no degree is specified, defaults to a little
        else:
            degree = "a little"
        
        if direction != None:
            direction = direction.lower()
            if direction == 'more':
                sign = 1
            else:
                sign = -1
        else:
            return # direction is required
        
        if color != None:
            color = color.lower()
        else:
            return # color is required
        
        # get current r g b values
        current_r = self.user_color.r
        current_g = self.user_color.g
        current_b = self.user_color.b
        
        # make target color from presets
        target_color = pygame.Color(self.preset_color_values[color][0],
                                self.preset_color_values[color][1], self.preset_color_values[color][2])
    
        # match the target color's brightness with the current brightness
        curr_v = self.user_color.hsva[2]
        target_color.hsva = (max(min(target_color.hsva[0], 360), 0),
                                max(min(target_color.hsva[1], 100), 0),
                                curr_v,
                                max(min(target_color.hsva[3], 100), 0))
        
        # get r g b values of target color
        target_r = target_color.r
        target_g = target_color.g
        target_b = target_color.b
        
        # add the r g b values
        weight = self.preset_degree_values[degree]/55.0
        
        r_sign = math.copysign(1.0, target_r - current_r)
        g_sign = math.copysign(1.0, target_g - current_g)
        b_sign = math.copysign(1.0, target_b - current_b)
        
        r_mean = (target_r + current_r)/2
        g_mean = (target_g + current_g)/2
        b_mean = (target_b + current_b)/2
        
        new_r = int(max(min(current_r + sign*r_sign*weight*r_mean, 255), 0))
        new_g = int(max(min(current_g + sign*g_sign*weight*g_mean, 255), 0))
        new_b = int(max(min(current_b + sign*b_sign*weight*b_mean, 255), 0))
        
        self.user_color = pygame.Color(new_r, new_g, new_b)
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
        
        return hex(self.user_color.r) + " " + hex(self.user_color.g) + \
            " " + hex(self.user_color.b)
                