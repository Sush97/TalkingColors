# Erik Ackermann
# Richard Boyle
# Kate Hansen
#
# SLP - Project 3
# Friday, April 20, 2012

# The main runtime program for our color picker system
# This file controls a color window that is updated by user input (via voice commands)
# 

import sys
import os
import pygame
from colorutil import *
ps_base = os.environ['PS_BASE']

# lab machine specific setup:
lab_machines = ['gatto', 'fluffy.cs.columbia.edu', 'cheshire',
              'veu', 'dinah', 'voix', 'voce.cs.columbia.edu',
              'chat', 'felix.cs.columbia.edu']
hostname = os.uname()[1]
if hostname in lab_machines:
    sys.path.append(ps_base + '/lib/python2.5/site-packages')
    import pocketsphinx as ps
else:
    import pocketsphinx as ps

am = ps_base + '/share/pocketsphinx/model/hmm/wsj1'

def main(argv):
    """ 
    """
    
    system_state = 'Greeting'
    consecutive_count = 0
    
    myState = ColorState()
    myState.init()
    pygame.init()
    
    while system_state != 'Exit':
        
        message = None
        # Initial prompt
        if system_state == 'Greeting':
            message = "Welcome to Talking Colors.  To begin, please pick a color."
            
            # speak the message
            speakMessage(message)
            
            # wait for user input, parse it
            
            # set state to this color
            #myState.update(this_color)
            
            system_state = 'Update State'
            continue
            
        # Start over prompt
        if system_state == 'New Color':
            message = "Pick a new color."
            
            # speak the message
            speakMessage(message)
            
            # wait for user input, parse it
            
            # set window to new color
            system_state = 'Update State'
            continue

        # update color prompt 
        elif system_state == 'Update State':
            if consecutive_count == 0:
                message = "How does this look?  You can adjust the color's brightness and saturation, or adjust the hue."
            
            elif consecutive_count == 1:
                message = "How does this look?"
            
            elif 1 < consecutive_count < 5:
                message = "How is this?"
            
            # speak the message
            speakMessage(message)
            
            # wait for input, parse it
        
            continue
    
    # prompt for output format
    prompt = "What output format would you like?  Available options are RGB and Hexidecimal.
    speakMessage(prompt)
        
    # wait for input, parse it
    
    # output (speak) the color in the specified format
    
    # Goodbye message
    goodbye_message = "Thanks!"

    


def speakMessage(message):
    """ Uses TTS system to speak a given string
    """
    
    

if __name__ == '__main__':
    main(sys.argv[1:])



