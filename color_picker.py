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
import string
#ps_base = os.environ['PS_BASE']

# lab machine specific setup:
#lab_machines = ['gatto', 'fluffy.cs.columbia.edu', 'cheshire',
#              'veu', 'dinah', 'voix', 'voce.cs.columbia.edu',
#              'chat', 'felix.cs.columbia.edu']
#hostname = os.uname()[1]
#if hostname in lab_machines:
#    sys.path.append(ps_base + '/lib/python2.5/site-packages')
#    import pocketsphinx as ps
#else:
#    import pocketsphinx as ps

#am = ps_base + '/share/pocketsphinx/model/hmm/wsj1'

def main(argv):
    """ Main method for the SDS system
    """
    
    system_state = 'Greeting'
    consecutive_count = 0
    
    myState = ColorState()
    myState.init()
    pygame.init()
    
    output_format = None
    
    while system_state != 'Exit':
        
        message = None
        # Initial prompt
        if system_state == 'Greeting':
            message = "Welcome to Talking Colors!  To begin, please pick a color.\nSay 'Help' at any time to hear a list of commands."
            
            # speak the message
            speakMessage(message)
            
            # wait for user input, parse it
            user_input = getUserInput()
            color = user_input["Color"]
            attribute = user_input["Attribute"]
            
            # set color state to this color
            myState.updateWithString(color, attribute)
            
            system_state = 'Update State'
            continue
            
        # Start over prompt
        elif system_state == 'New Color':
            message = "Pick a new color."
            
            # speak the message
            speakMessage(message)
            
            # wait for user input, parse it
            user_input = getUserInput()
            color = user_input["Color"]
            attribute = user_input["Attribute"]
            
            # set color state to this color
            myState.updateWithString(color, attribute)

            # reset consecutive_count to 1
            consecutive_count = 1
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
            else:
                message = "Look good?"
            
            # speak the message
            speakMessage(message)
            
            # wait for input, parse it
            user_input = getUserInput()
            color = user_input["Color"]
            attribute = user_input["Attribute"]
            degree = user_input["Degree"]
            direction = user_input["Direction"]
            output_format = user_input["Output Format"]
            help = user_input["Help"]
            start_over = user_input["Start Over"]
            exit = user_input["Exit"]
                
            if help != None:
                system_state = 'Help'
                continue # go there now
            
            if start_over != None:
                system_state = 'New Color'
                continue # go there now
                        
            if attribute != None:
                myState.changeAttribute(attribute, degree, direction)
            
            if color != None:
                myState.adjustColor(color, degree, direction)
                
            # if user is done, set state to 'Exit'
            elif exit != None:
                print("exiting...")
                system_state = 'Exit'
            # else system state remains unchanged and we increment consecutive count
            else:
                consecutive_count += 1
            continue
            
        elif system_state == 'Help':
            message = "... Would you like to start over or continue with your current color?"
            
            # speak the message
            speakMessage(message)
            
            # wait for input, parse it
            getUserInput()
            
            # set system state based on what the user says
            
            continue
    
    # if unspecified, prompt for output format
    first_try = True
    while output_format == None:
        if first_try:
            prompt = "What output format would you like?  Available options are RGB and Hexidecimal."     
        else:
            prompt = "I'm sorry, I didn't understand that.  Available options are RGB and Hexidecimal."
            
        speakMessage(prompt)
        output_format = getUserInput()["Output Format"]
            
    
    # output (speak) the color in the specified format
    message = "Your color is "
    if output_format == "HEX" or output_format == "HEXADECIMAL":
        message += myState.getHEX()
    elif output_format == "RGB":
        message += myState.getRGB()
    
    speakMessage(message)
    
    # Goodbye message
    goodbye_message = "Thanks for using Talking Colors!"
    speakMessage(goodbye_message)
    

def speakMessage(message):
    """ Uses TTS system to speak a given string
    """
    
    print(message)
    
    # use subprocess to run a perl script?
    

def getUserInput():
    """ Uses autorecord and saves message.
        Then the decoder turns this message into a string.
        Then, we recognize the concepts and return a dictionary.
    """
    
    #decoder = ps.Decoder(am, os.path.join(path, grammar_file), 
    #                os.path.join(path, dictionary_file))
    
    # Run autorecord
    # ...
    
    # Run the Recognizer
    #fh = file(wav_file, 'rb')
    #decoder.decode_raw(fh)
    #result = decoder.get_hyp()
    #fh.close()
    
    #output = result.split("'")
    #concept_table = createConceptTable(output[1])
    
    # for now...
    user_input = str(raw_input("User input: "))
    user_input = user_input.upper()
    
    # strip punctuation (only necessary with typed input)
    exclude = set(string.punctuation)
    user_input = ''.join(ch for ch in user_input if ch not in exclude)
    concept_table = createConceptTable(user_input)
    # create the concept dictionary
    concept_dict = {"Color": concept_table[0],
                    "Attribute": concept_table[1],
                    "Degree": concept_table[2],
                    "Direction": concept_table[3],
                    "Output Format": concept_table[4],
                    "Help": concept_table[5],
                    "Start Over": concept_table[6],
                    "Exit": concept_table[7]}
    #print(concept_dict)
    
    if all(val == None for val in concept_dict.values()):
        print("Sorry, I didn't understand")
        # query again, display friendly message
        
    return concept_dict
    
def createConceptTable(output):
    """ Takes output string and returns a dictionary representing the concept table
    """

    colors = ["RED", "ORANGE", "YELLOW", "GREEN", "BLUE", \
        "PURPLE", "BLACK", "WHITE", "GREY", "PINK", "GRAY"]
    attributes = ["BRIGHTER", "LIGHTER", "LIGHT", "DARKER", \
        "BRIGHT", "DARK", "SATURATED", "DESATURATED"]
    degrees = ["A LOT", "MUCH", "A LITTLE", "A TINY BIT"]
    directions = ["MORE", "LESS"]
    output_formats = ["HEX", "RGB"]
    help = ["HELP"]
    start_over = ["START OVER", "RESTART"]
    exit = ["QUIT", "STOP", "DONE", "EXIT"]
    
    lists = [colors, attributes, degrees, directions, output_formats, help, start_over, exit]

    output_table = [None, None, None, None, None, None, None, None]

    for x in degrees:
        if x in output:
            output_table[2] = x
    
    for x in start_over:
        if x in output:
            output_table[6] = x

    output = output.split()
    for x in output:
        for i in [0, 1, 3, 4, 5, 7]:
            for y in lists[i]:
                if x == y:
                    output_table[i] = y

    return output_table

if __name__ == '__main__':
    main(sys.argv[1:])



