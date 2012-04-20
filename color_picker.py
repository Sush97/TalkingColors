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
import subprocess
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
    """ Main method for the SDS system
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
            message = "Welcome!  To begin, please pick a color. \
                Say 'Help' at any time to hear a list of commands"
            
            # speak the message
            speakMessage(message)
            
            # wait for user input, parse it
            color = getUserInput()["Color"]
            
            # set color state to this color
            myState.updateWithString(color)
            
            system_state = 'Update State'
            continue
            
        # Start over prompt
        if system_state == 'New Color':
            message = "Pick a new color."
            
            # speak the message
            speakMessage(message)
            
            # wait for user input, parse it
            color = getUserInput()["Color"]
            
            # set color state to this color
            myState.updateWithString(color)

            system_state = 'Update State'
            
            # reset consecutive_count to 1
            consecutive_count = 1
            
            continue

        # update color prompt 
        elif system_state == 'Update State':
            if consecutive_count == 0:
                message = "How does this look?  You can adjust the color's brightness and saturation, or adjust the hue."
            elif consecutive_count == 1:
                message = "How does this look?"
            elif 1 < consecutive_count < 5:
                message = "How is this?"
            else:
                message = "Look good?"
            
            # speak the message
            speakMessage(message)
            
            # wait for input, parse it
            getUserInput()
            
            # if user is done, set state to 'Exit'
            if :
            # else system state remains unchanged
            # and we increment consecutive count
            else:
                consecutive_count += 1
            continue
            
        elif system_state == 'Help':
            message = ""
            
            # speak the message
            speakMessage(message)
            
            # wait for input, parse it
            getUserInput()
            
            # set system state based on what the user says
            
            continue
    
    # prompt for output format
    prompt = "What output format would you like?  Available options are RGB and Hexidecimal.
    speakMessage(prompt)
        
    # wait for input, parse it
    format = getUserInput()["Output Format"]
    
    # output (speak) the color in the specified format
    message = "Your color is "
    if format == "HEX" or format == "HEXADECIMAL":
        message += myState.getHEX()
    elif format == "RGB"
        message += myState.getRGB()
    
    speakMessage(message)
    
    # Goodbye message
    goodbye_message = "Thanks!"
    speakMessage(goodbyeMessage)
    

def speakMessage(message):
    """ Uses TTS system to speak a given string
    """
    
    # use subprocess to run a perl script?
    

def getUserInput():
    """ Uses autorecord and saves message.
        Then the decoder turns this message into a string.
        Then, we recognize the concepts and return a dictionary.
    """
    
    decoder = ps.Decoder(am, os.path.join(path, grammar_file), 
                    os.path.join(path, dictionary_file))
    
    # Run autorecord
    # ...
    
    # Run the Recognizer
    fh = file(wav_file, 'rb')
    decoder.decode_raw(fh)
    result = decoder.get_hyp()
    fh.close()
    
    output = result.split("'")
    
    # create the concept dictionary
    concept_table = createConceptTable(output[1])
    concept_dict = {"Color": concept_table[0],
                    "Attribute": concept_table[0],
                    "Degree": concept_table[0],
                    "Direction": concept_table[0],
                    "Output Format": concept_table[0]}
    
    return concept_dict
    
def createConceptTable(output):
    """ Takes output string and returns a dictionary representing the concept table
    """

    colors = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE", \
        "PURPLE", "BLACK", "WHITE", "GREY", "PINK"]
    attributes = ["BRIGHTER", "DARKER", "BRIGHT", "DARK", "SATURATED", "DESATURATED"]
    degrees = ["A LOT", "MUCH", "A LITTLE", "A TINY BIT"]
    directions = ["MORE", "LESS"]
    output_formats = ["HEX", "RGB"]
    
    lists = [colors, attributes, degrees, directions, output_formats]

    output_table = ["UNSPECIFIED", "UNSPECIFIED", "UNSPECIFIED", "UNSPECIFIED","UNSPECIFIED"]

    for x in degrees:
        if x in output:
            output_table[2] = x

    output = output.split()
    for x in output:
        for i in [0, 1, 3, 4]:
            for y in lists[i]:
                if x == y:
                    output_table[i] = y

    return formatTable(output_table)

if __name__ == '__main__':
    main(sys.argv[1:])



