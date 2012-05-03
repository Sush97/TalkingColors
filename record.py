#!/usr/bin/python

"""
Usage:  record.py <threshold>
Output: a wave file (input.wav)
============================================================
This is a Python script that uses pyAudio + portaudio 1.9 to 
record an utterance and save it to a wave file. The program 
automatically detecs a period of silence and stops after 1 
second of silence.  Waits 2 seconds before starting detection.

Audio is read at 2048 frames per read unit, which means 
roughly 8 reads per second. The program calculates the RMS
of amplitudes for the last .5 seconds.

We set the default "silence threshold" RMS value to 250
(speaking to the mic usually makes the value jump to 600)
This can be changed using the command-line argument.

Ben Mann
Cipta Herwana
Spoken Language Processing Spring 2010
"""

import wave, sys, os
from struct import *
import subprocess

current = os.getcwd()
# os.chdir('/proj/speech/tools/autorecord')
sys.path.append('/proj/speech/tools/autorecord-64bit/pyaudio/lib/python2.6/site-packages')

import pyaudio

os.chdir(current)
  

def record(thresh=250, verbose=True, path='./input.wav'):
    """
    Set verbose = False to supress stdout
    """

    chunk = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    TIMEOUT = 20
    WAVE_OUTPUT_FILENAME = path

    # open stream
    p = pyaudio.PyAudio()

    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)

    if verbose:
        print "* recording"
    all = []
    sumsq = [0.0] * 4

    ndata = len(sumsq) * chunk
    silencecount = 0
    statlen = 0

    # RATE / chunk = reads per second
    reads_per_sec = RATE / chunk
    for time in xrange(reads_per_sec * TIMEOUT):
        data = stream.read(chunk)
        all.append(data)
        # amplitude measurement
        window = unpack('%dh'%(chunk),data) # size = chunk
        
        sumsq = sumsq[1:]
        sumsq.append(sum([x**2 for x in window]))
        intensity = (sum(sumsq) / ndata) ** .5 # RMS
        
        if intensity < thresh: # looks silent
            silencecount += 1
        else:
            silencecount = 0
            
        if verbose:
            base = int(thresh/50)
            total = int(intensity/50)
            if total > base:
                statusbar = base*'=' + (total-base)*'-'
            else:
                statusbar = total*'='
            out = str(silencecount).ljust(3) + str.ljust(str(int(intensity)), 5) + '[' \
                + statusbar + ']'
            if statlen != 0:
                print '\r',
                sys.stdout.flush()
                print ' ' *(statlen),
                print '\r',
            print out,
            sys.stdout.flush()
            statlen = len(out)
        

        if time > 2 * reads_per_sec and silencecount > reads_per_sec:
            break
            
    if verbose:
        print
        print "* done recording"

    stream.close()
    p.terminate()

    # write data to WAVE file
    data = ''.join(all)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()
    
# run as script
if __name__ == '__main__':
    if len(sys.argv) ==2:
        thresh = int(sys.argv[1])
        record(thresh=thresh)
    else:
        record()
