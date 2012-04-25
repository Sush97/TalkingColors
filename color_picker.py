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
from random import choice
from record import *
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

am = ps_base + '/share/pocketsphinx/model/hmm/en_US/hub4_16k_4000s'

def main(argv):
    """ Main method for the SDS system
    """
    
    system_state = 'Greeting'
    system_output_format = None
    consecutive_count = 0
    error_last = False
    positive_last = False
    negative_last = False
    
    myState = ColorState()
    myState.init()
    pygame.init()

    path = "/home/kmh2151/TalkingColors/ASR/"
    grammar_file = "gram.jsgf"
    dictionary_file = "wlist5o.dic"

    # initialize decoder
    decoder = ps.Decoder(hmm=am, jsgf=os.path.join(path, grammar_file), 
                    dict=os.path.join(path, dictionary_file))

    while system_state != 'Exit':
       
        message = None
        # Initial prompt
        if system_state == 'Greeting':

            message = "Welcome to Talking Colors!  To begin, please pick a color.\nSay Help at any time to hear a list of commands."
                    
            # speak the message
            speakMessage(message)

            # get user input
            user_input = getUserInput(decoder)
            color = user_input["Color"]
            attribute = user_input["Attribute"]
            degree = user_input["Degree"]
            direction = user_input["Direction"]
            output_format = user_input["Output Format"]
            help = user_input["Help"]
            start_over = user_input["Start Over"]
            exit = user_input["Exit"]
            undo = user_input["Undo"]
            positive = user_input["Positive"]
            negative = user_input["Negative"]
            
            if color != None:
                # set color state to this color
                myState.updateWithString(color, attribute)
            elif help != None:
                system_state = 'Help'
                continue # go there now
            else:
                system_state = 'New Color'
                continue # go there now

            system_state = 'Update State'
            continue
            
        # Start over prompt
        elif system_state == 'New Color':
            message = "Ok, let's start over.  Pick a new color."
            
            # speak the message
            speakMessage(message)

            # get user input
            user_input = getUserInput(decoder)
            color = user_input["Color"]
            attribute = user_input["Attribute"]
            degree = user_input["Degree"]
            direction = user_input["Direction"]
            output_format = user_input["Output Format"]
            help = user_input["Help"]
            start_over = user_input["Start Over"]
            exit = user_input["Exit"]
            undo = user_input["Undo"]
            positive = user_input["Positive"]
            negative = user_input["Negative"]
            
            if undo != None:
                myState.undo()
                system_state = 'Update State'
                continue # go there now
            elif color != None:
                # set color state to this color
                myState.updateWithString(color, attribute)
            elif help != None:
                system_state = 'Help'
                continue # go there now
            else:
                system_state = 'New Color'
                continue # go there now

            # reset consecutive_count to 1
            consecutive_count = 1
            system_state = 'Update State'
            continue

        # update color prompt 
        elif system_state == 'Update State':
            if error_last == True:
                message = "Try again please, or say help for more options."
                error_last = False
            elif positive_last == True:
                message = "If you're done, say Exit, or you can keep making changes."
                positive_last = False
            elif negative_last == True:
                message = "You can say Undo, Start Over or you can keep making changes from here."
                negative_last = False
            elif consecutive_count == 0:
                message = "How does this look?  You can adjust the color's brightness and saturation, or adjust the hue."            
            elif consecutive_count == 1:
                message = "How does this look?"
            else:
                message = choice(["How is this?",
                                "Is this good?",
                                "Look good?",
                                "Ooh, that's nice.  Look good?",
                                "Looking good!"])
            
            # speak the message
            speakMessage(message)

            # get user input
            user_input = getUserInput(decoder)
            color = user_input["Color"]
            attribute = user_input["Attribute"]
            degree = user_input["Degree"]
            direction = user_input["Direction"]
            output_format = user_input["Output Format"]
            help = user_input["Help"]
            start_over = user_input["Start Over"]
            exit = user_input["Exit"]
            undo = user_input["Undo"]
            positive = user_input["Positive"]
            negative = user_input["Negative"]

            # update count
            consecutive_count += 1
            
            if help != None:
                system_state = 'Help'
                continue

            if undo != None:
                if not myState.undo():
                    message = "You can't undo any further"
                    speakMessage(message)
                continue # stay in this state
            
            if start_over != None:
                system_state = 'New Color'
                continue # go there now

            if attribute != None:
                # check if color has changed
                if not myState.changeAttribute(attribute, degree, direction):
                    if direction == None:
                        direction = ""
                    else:
                        direction += " "
                    # display message if color is at extremes (and can't be changed)
                    message = "I can't make the color any " + direction.lower() + attribute.lower()
                    speakMessage(message)
                    error_last = True
                    continue
            
            if color != None:
                # check if color has changed
                if not myState.adjustColor(color, degree, direction):
                    if direction == None:
                        direction = ""
                    else:
                        direction += " "
                    # display message if color is at extremes (and can't be changed)
                    message = "I can't make the color any " + direction.lower() + color.lower()
                    speakMessage(message)
                    error_last = True
                    continue
        
            if negative != None:
                negative_last = True
                continue

            if positive != None:
                positive_last = True
                continue

            if output_format != None:
                system_output_format = output_format
    
            # if user is done, set state to 'Exit'
            if exit != None:
                print("exiting...")
                system_state = 'Exit'
            continue
            
        elif system_state == 'Help':
            message = "Say a command to change the state of your color. You can alter a color's brightness, saturation, or hue. If at any point you want to undo your last command, say Undo. When you are satisfied with your color, say Done. Would you like to start over or continue with your current color?"           

            # speak the message
            speakMessage(message)

            # get user input
            user_input = getUserInput(decoder)
            color = user_input["Color"]
            attribute = user_input["Attribute"]
            degree = user_input["Degree"]
            direction = user_input["Direction"]
            output_format = user_input["Output Format"]
            help = user_input["Help"]
            start_over = user_input["Start Over"]
            exit = user_input["Exit"]
            undo = user_input["Undo"]
            positive = user_input["Positive"]
            negative = user_input["Negative"]

            if start_over != None:
                system_state = 'New Color'
                continue
            
            elif exit != None:
                system_state = 'Exit'
                continue

            elif positive != None:
                if len(myState.user_color) == 0:
                    system_state = 'Greeting'
                else:
                    system_state = 'Update State'
                continue
            
            else:
                system_state = 'Help'


            # set system state based on what the user says
            # either go to New Color or Update State
            
            continue
    
    # if unspecified, prompt for output format
    first_try = True
    while system_output_format == None:
        if first_try:
            prompt = "What output format would you like?  Available options are RGB and Hexidecimal."     
        else:
            prompt = "I'm sorry, I didn't understand that.  Available options are RGB and Hexidecimal."
            
        speakMessage(prompt)
        output_format = getUserInput(decoder)["Output Format"]
        system_output_format = output_format
            
    
    # output (speak) the color in the specified format
    message = ""
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
    
    # use subprocess to run a perl script
    # script generates wave file from string
    perl_script_path = "/home/kmh2151/TalkingColors/TTS/speak.pl"

    command = ["perl", perl_script_path, message] # saves wav file to output.wav
    subprocess.call(command, stdin=None, stdout=None, stderr=None, shell=False)
    
    # use subprocess to play wav file
    fnull = open(os.devnull, 'w')
    command = ["play", "./TTS/output.wav"] # plays wav file
    subprocess.call(command, stdin=None, stdout=fnull, stderr=fnull, shell=False)
    fnull.close()
    
    

def getUserInput(decoder):
    """ Uses autorecord and saves message.
        Then the decoder turns this message into a string.
        Then, we recognize the concepts and return a dictionary.
    """
    
    path = "/home/kmh2151/TalkingColors/"

    record()
    
    wav_file = os.path.join(path, "input.wav")
    
    # Run the Recognizer
    fh = file(wav_file, 'rb')
    decoder.decode_raw(fh)
    result = decoder.get_hyp()[0]
    fh.close()
    
    print("result:")
    print(result)

    if result == None:
        message = "Sorry, I didn't understand"
        speakMessage(message)
        # query again
        return getUserInput(decoder)

    concept_table = createConceptTable(result)
    
    # for text input
    #user_input = str(raw_input("User input: "))
    #user_input = user_input.upper()
    
    # strip punctuation (only necessary with typed input)
    #exclude = set(string.punctuation)
    #user_input = ''.join(ch for ch in user_input if ch not in exclude)
    #concept_table = createConceptTable(user_input)

    # create the concept dictionary
    concept_dict = {"Color": concept_table[0],
                    "Attribute": concept_table[1],
                    "Degree": concept_table[2],
                    "Direction": concept_table[3],
                    "Output Format": concept_table[4],
                    "Help": concept_table[5],
                    "Start Over": concept_table[6],
                    "Exit": concept_table[7],
                    "Undo": concept_table[8],
                    "Positive": concept_table[9],
                    "Negative": concept_table[10]}
    #print(concept_dict)
    
    if all(val == None for val in concept_dict.values()):
        message = "Sorry, I didn't understand"
        speakMessage(message)
        # query again
        return getUserInput(decoder)
        
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
    output_formats = ["HEX", "RGB", "HEXADECIMAL"]
    help = ["HELP"]
    start_over = ["START OVER", "RESTART"]
    exit = ["QUIT", "STOP", "DONE", "EXIT"]
    color_adjs = ["REDDER", "REDDISH", "ORANGER", "ORANGISH", "YEllOWER", "YELLOWISH", \
        "GREENER", "GREENISH", "BLUER", "BLUISH", "PURPLER", "PURPLISH", "BLACKISH", \
        "BLACKER", "WHITISH", "WHITER", "GREYISH", "GREYER", "PINKISH", "PINKER"]
    undo = ["UNDO", "CANCEL", "GO BACK"]
    navigation_positive = ["YES", "GOOD", "OK", "CONTINUE"]
    navigation_negative = ["NO", "BAD", "NOPE"]
        
    lists = [colors + color_adjs, attributes, degrees, directions, \
        output_formats, help, start_over, exit, undo, navigation_positive, navigation_negative]

    output_table = [None, None, None, None, None, None, None, None, None, None, None]

    for x in degrees:
        if x in output:
            output_table[2] = x
    
    for x in start_over:
        if x in output:
            output_table[6] = x

    output = output.split()
    for x in output:
        for i in [0, 1, 3, 4, 5, 7, 8, 9, 10]:
            for y in lists[i]:
                if x == y:
                    output_table[i] = y

    return output_table

if __name__ == '__main__':
    main(sys.argv[1:])



