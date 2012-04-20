#!/usr/bin/python

# Recognition Script for Project Part 2.

import sys
import os
from optparse import OptionParser
ps_base = os.environ['PS_BASE']

# lab machine specific setup:
lab_machines=['gatto', 'fluffy.cs.columbia.edu', 'cheshire',
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

    # Parse command line arguments
    usage = 'Usage: ./recognize_wav.py <wavfile> [options]'
    parser = OptionParser(usage)

    # -g grammar
    ghelp = 'Filename of the .jsgf grammar to use.  '
    ghelp += 'The default name is gram.jsgf'
    parser.add_option('-g', '--gram', action='store',
                      type='string', dest='gram',
                      help=ghelp, default='gram.jsgf',
                      metavar='GRAM')

    # -d dictionary
    dhelp = 'Filename of the pronunciation dictionary to use.  '
    dhelp += 'The default is WSJ.'
    default_dict = ps_base + '/share/pocketsphinx/model/lm/wsj/wlist5o.dic'
    parser.add_option('-d', '--dict', action='store',
                      type='string', dest='dict',
                      help=dhelp, default=default_dict,
                      metavar='DICT')

    # -a acoustic model
    ahelp = 'Number of the acoustic model to use.  '
    dhelp += 'The default is 1.'
    parser.add_option('-a', '--am', action='store',
                      type='string', dest='am',
                      help=ahelp, default='1',
                      metavar='AM')

    (options, args) = parser.parse_args(argv)
    if len(args) != 1:
        parser.error(usage)
    wav_file = args[0]

    # ACOUSTIC MODELS:
    # 1: the default WSJ-trained one
    # 2: HUB4 Broadcast News, 4000 senones
    # 3: HUB4 Broadcast News, 6000 senones
    # 4: WSJ, 8000 senones, 1 gaussian
    # 5: WSJ, 8000 senones, 4 gaussians
    # 6: WSJ, 8000 senones, 16 gaussians
    # 7: WSJ, 8000 senones, 256 gaussians

    ams = {'1': ps_base + '/share/pocketsphinx/model/hmm/wsj1',
           '2': ps_base + '/share/pocketsphinx/model/hmm/en_US/hub4_16k_4000s',
           '3': ps_base + '/share/pocketsphinx/model/hmm/en_US/hub4_16k_6000s',
           '4': ps_base +
           '/share/pocketsphinx/model/hmm/us/sphinx_wsj_all_cont_3no_8000_1',
           '5': ps_base +
           '/share/pocketsphinx/model/hmm/us/sphinx_wsj_all_cont_3no_8000_4',
           '6': ps_base +
           '/share/pocketsphinx/model/hmm/us/sphinx_wsj_all_cont_3no_8000_16',
           '7': ps_base +
           '/share/pocketsphinx/model/hmm/us/sphinx_wsj_all_semi_3no_8000_256'}

    decoder = None
    # Different options are required depending on which AM is used.
    # First 3 just requre hmm, jsgf, and dict
    if options.am in ['1', '2', '3']:
        decoder = ps.Decoder(hmm=ams[options.am],
                             jsgf=options.gram,
                             dict=options.dict)

    # The other four require some extra args
    elif options.am == '4':
        decoder = ps.Decoder(
            hmm=ams['4']+'/model_parameters/wsj_all_cont_3no_8000_1.cd',
            mdef=ams['4']+'/model_architecture/wsj_all_cont_3no_8000.mdef',
            feat='1s_12c_12d_3p_12dd',
            jsgf=options.gram,
            dict=options.dict)
    elif options.am == '5':
        decoder = ps.Decoder(
            hmm=ams['5']+'/model_parameters/wsj_all_cont_3no_8000_4',
            mdef=ams['5']+'/model_architecture/wsj_all_cont_3no_8000.mdef',
            feat='1s_12c_12d_3p_12dd',
            jsgf=options.gram,
            dict=options.dict)
    elif options.am == '6':
        decoder = ps.Decoder(
            hmm=ams['6']+'/model_parameters/wsj_all_cont_3no_8000_16',
            mdef=ams['6']+'/model_architecture/wsj_all_cont_3no_8000.mdef',
            feat='1s_12c_12d_3p_12dd',
            jsgf=options.gram,
            dict=options.dict)
    elif options.am == '7':
        decoder = ps.Decoder(
            hmm=ams['7']+'/model_parameters/wsj_all_semi_3no_8000_256',
            mdef=ams['7']+'/model_architecture/wsj_all_cont_3no_8000.mdef',
            feat='s2_4x',
            jsgf=options.gram,
            dict=options.dict)
    else:
        parser.error('Please specify a number 1-7 for the acoustic model.')

    # Run the Recognizer
    fh = file(wav_file, 'rb')
    decoder.decode_raw(fh)
    result = decoder.get_hyp()
    fh.close()

    print
    print 'ASR Result:', result

if __name__ == '__main__':
    main(sys.argv[1:])



