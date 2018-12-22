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

TAG_MAP = {
    'CC': {'pos': 'NOUN'},
    'CL': {'pos': 'NOUN'},
    'DEM': {'pos': 'NOUN'},
    'ECH': {'pos': 'NOUN'},
    'INJ': {'pos': 'NOUN'},
    'INTF': {'pos': 'NOUN'},
    'INTJ': {'pos': 'NOUN'},
    'J': {'pos': 'ADJ'},
    'JJ': {'pos': 'ADJ'},
    'NN': {'pos': 'NOUN'},
    'NNP': {'pos': 'NOUN'},
    'NNPP': {'pos': 'NOUN'},
    'NP': {'pos': 'NOUN'},
    'NST': {'pos': 'NOUN'},
    'PRP': {'pos': 'NOUN'},
    'PSP': {'pos': 'NOUN'},
    'QC': {'pos': 'NOUN'},
    'QF': {'pos': 'NOUN'},
    'QO': {'pos': 'NOUN'},
    'RB': {'pos': 'NOUN'},
    'RDP': {'pos': 'NOUN'},
    'RM': {'pos': 'NOUN'},
    'RP': {'pos': 'NOUN'},
    'SY': {'pos': 'NOUN'},
    'SYM': {'pos': 'SYM'},
    'UNK': {'pos': 'NOUN'},
    'UT': {'pos': 'NOUN'},
    'VAUX': {'pos': 'VERB'},
    'VM': {'pos': 'VERB'},
    'WQ': {'pos': 'NOUN'}
}



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
    parser.add_argument("-i", "--input_file", dest="test_data", type=str, metavar='<str>', required=False,
                        help="Test data path ex: data/test/telugu/test.txt")
    parser.add_argument("-s", "--sent_split", dest="sent_split", type=str, metavar='<str>', required=False,
                        help="Test data path ex: data/test/telugu/test.txt",
                        default=True)
    parser.add_argument("-o", "--output_file", dest="output_path", type=str, metavar='<str>',
                         help="The path to the output file",
                         default=path.join(path.dirname(path.abspath(__file__)), "outputs", "output_file"))
    return parser.parse_args()

def pipeline():
    """Create a new model, set up the pipeline and train the tagger. In order to
    train the tagger with a custom tag map, we're creating a new Language
    instance with a custom vocab.
    """
    args = get_args()
    print(args)
    curr_dir = path.dirname(path.abspath(__file__))
    lang = args.language
    print(lang)
    output_dir = path.join(path.dirname(path.abspath(__file__)), "outputs")
    if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    model_path = "%s/spacymodels/%s/%s.model" % (curr_dir, args.language,  args.tag_type)    
    data_path = "%s/data/train/%s/train.%s.conll" % (curr_dir, args.language, args.encoding)

    file = open(data_path, "r")
    TRAIN_DATA= spacy_data_reader.spacy_load_data(data_path)

    nlp = spacy.blank(lang)
    # add the tagger to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    tagger = nlp.create_pipe('tagger')
    # Add the tags. This needs to be done before you start training.
    for tag, values in TAG_MAP.items():
        tagger.add_label(tag, values)
    nlp.add_pipe(tagger)

    optimizer = nlp.begin_training()
    for i in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        # batch up the examples using spaCy's minibatch
        batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
        for batch in batches:
            texts, annotations = zip(*batch)
            nlp.update(texts, annotations, sgd=optimizer, losses=losses)
        print('Losses', losses)

    # test the trained model
    test_text = "నా నా కధ అందరి అందరి ఆడపిల్లల కధే ."
    doc = nlp(test_text)
    print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the save model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        doc = nlp2(test_text)
        print('Tags', [(t.text, t.tag_, t.pos_) for t in doc])

if __name__ == '__main__':
    pipeline()
