#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding
import re
import os
import tagger.src.spacy_data_reader as spacy_data_reader
import argparse
import sys, os.path as path



def get_args():
    ''' This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(description='Scorer pipeline')

    parser.add_argument("-l", "--language", dest="language", type=str, metavar='<str>', required=True,
                         help="Language of the dataset: tel (telugu), hin (hindi), tam (tamil), kan (kannada), pun (pubjabi)")
    parser.add_argument("-t", "--tag_type", dest="tag_type", type=str, metavar='<str>', required=True,
                         help="Tag type: pos, chunk, parse")
    parser.add_argument("-e", "--encoding", dest="encoding", type=str, metavar='<str>', required=False,
                        help="Encoding of the data (utf, wx)",
                        default="utf")
    parser.add_argument("-v", "--version", dest="version", type=str, metavar='<str>', required=False,
                        help="Version",
                        default="0.0.0")
    return parser.parse_args()

def pipeline():
    args = get_args()
    curr_dir = path.dirname(path.abspath(__file__))
    lang = args.language
    #output_dir = "%s/spacypackages/%s/%s" % (curr_dir, args.language,  args.tag_type)    
    output_dir = "%s/spacypackages/%s_model-%s/%s_model/%s_model-%s" % (curr_dir, args.language,  args.version, args.language, args.language,  args.version)   
    test_text = input("Enter Sentence:")
    #test_text = "నా నా కధ అందరి అందరి ఆడపిల్లల కధే ."
    nlp2 = spacy.load(output_dir)
    doc = nlp2(test_text)
    print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])

if __name__ == '__main__':
    pipeline()
