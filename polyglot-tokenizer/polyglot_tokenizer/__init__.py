#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""Tokenizer for world's most spoken languages.

This module provides a tokenizer for world's most spoken languages and social
media texts like facebook, twitter etc.

Copyright (c) 2015-2018 Irshad Ahmad
<irshad.bhat@research.iiit.ac.in>
"""

import io
import sys
import codecs
import argparse

from .tokenizer import Tokenizer

__all__ = ['Tokenizer']
__version__ = '1.0'


def parse_args(args):
    prog = 'indic-tokenizer'
    description = "Tokenizer for world's most spoken languages"
    languages = '''hi ur bn as gu ml pa te ta kn or mr cu myv nn yi
                ne bo br ks en es ca cs de el en fi da eu kok nb uz
                fr ga hu is it lt lv nl pl pt ro ru sk bm yue mk ku
                sl sv zh et fo gl hsb af ar be hy bg ka ug hr mn tk
                kk ky la no fa uk tl tr vi yo ko got ckb he id sr'''.split()
    lang_help = 'select language (2 letter ISO-639 code) {%s}' % (
                ', '.join(languages))
    # parse command line arguments
    parser = argparse.ArgumentParser(prog=prog,
                                     description=description)
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%s %s' % (prog, __version__))
    parser.add_argument('-i',
                        '--input',
                        metavar='',
                        dest='infile',
                        type=str,
                        help='<input-file>')
    parser.add_argument('-s',
                        '--split-sentences',
                        dest='split_sen',
                        action='store_true',
                        help='set this flag to apply'
                             ' sentence segmentation')
    parser.add_argument('-t',
                        '--social-media-test',
                        dest='smt',
                        action='store_true',
                        help='set this flag if the input file contains '
                             'social media text like twitter, facebook '
                             'and whatsapp')
    parser.add_argument('-o',
                        '--output',
                        metavar='',
                        dest='outfile',
                        type=str,
                        help='<output-file>')
    parser.add_argument('-l',
                        '--language',
                        metavar='',
                        dest='lang',
                        choices=languages,
                        default='en',
                        help=lang_help)
    args = parser.parse_args(args)
    return args


def get_file_pointers(args):
    if args.infile:
        ifp = io.open(args.infile, encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ifp = codecs.getreader('utf8')(sys.stdin.buffer)
        else:
            ifp = codecs.getreader('utf8')(sys.stdin)

    if args.outfile:
        ofp = io.open(args.outfile, mode='w', encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ofp = codecs.getwriter('utf8')(sys.stdout.buffer)
        else:
            ofp = codecs.getwriter('utf8')(sys.stdout)
    return ifp, ofp


def process_args(args):
    ifp, ofp = get_file_pointers(args)

    # initialize tokenizer
    tok = Tokenizer(lang=args.lang,
                    smt=args.smt,
                    split_sen=args.split_sen,
                    from_file=True)

    # tokenize
    for line in ifp:
        line = tok.tokenize(line)
        if args.split_sen:
            line = '\n'.join([' '.join(sen) for sen in line])
        else:
            line = ' '.join(line)
        ofp.write('%s\n' % line)

    # close files
    ifp.close()
    ofp.close()


def main():
    # parse arguments
    args = parse_args(sys.argv[1:])
    process_args(args)
