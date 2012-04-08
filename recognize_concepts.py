# Erik Ackermann
# Richard Boyle
# Kate Hansen
#
# SLP - Project 2
# Friday, March 30, 2012

# This program takes a .wav file, runs the ASR system, and generates the concept tables

import sys
import subprocess
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: {0} <wav file>".format(sys.argv[0]))
        sys.exit("Incorrect number of arguments")

    path = "/proj/speech/users/cs4706/asrhw/kmh2151/"
    grammar_file = "gram.jsgf"
    dictionary_file = "wlist5o.dic"

    f = open(sys.argv[1], 'r')
    command = ["/proj/speech/users/cs4706/pasr/recognize_wav.py", str(sys.argv[1]), "-g",\
             os.path.join(path, grammar_file), "-a", "2", "-d", os.path.join(path, dictionary_file)]
    process = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)    
    output = process.communicate()[0]

    output = output.split("'")
    print("Our output:")
    print(output[1])

    concept_file = open("concept_table.txt", 'w')
    concept_file.write(output[1] + "\n\n")
    concept_file.write(createConceptTable(output[1]))
    concept_file.close()

    f.close()

def createConceptTable(output):
    """ Takes output string and returns a string representing the concept table
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

def formatTable(output_table):
    """ Formats the string into a table (also a string)
    """
       
    table = ""
    table += "Color:\t\t\t" + output_table[0] + "\n"
    table += "Attribute:\t\t" + output_table[1] + "\n"
    table += "Degree:\t\t\t" + output_table[2] + "\n"
    table += "Direction:\t\t" + output_table[3] + "\n"
    table += "Output Format:\t" + output_table[4] + "\n"

    return table

if __name__ == "__main__": # Default "main method" idiom.
    main()

# Color:
# Attribute:
# Degree:
# Direction:
# Output Format:

