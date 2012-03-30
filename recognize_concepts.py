# Erik Ackermann
# Richard Boyle
# Kate Hansen
#
# SLP - Project 2
# Friday, March 30, 2012

# This program takes a .wav ﬁle, runs the ASR system, and generates the concept tables

import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: {0} <wav file>".format(sys.argv[0]))
        sys.exit("Incorrect number of arguments")

    f = open(sys.argv[1], 'r')
    
    concept_file = open("concept_table.txt", 'w')

if __name__ == "__main__": # Default "main method" idiom.
    main()