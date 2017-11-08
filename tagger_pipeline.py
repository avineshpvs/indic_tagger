'''
Pipeline code for Indic Tagger

Example:
python tagger_pipeline.py -p train -o outputs -l telugu -t pos -m crf -i data/test/telugu/test.wx.ssf -e wx

    -p, --pipeline_type - train, test, predict
    -l, --language      - tel, hin, tam, pun
    -t, --tag_type      - pos, chunk
    -m, --model_type    - crf, hmm, cnn, lstm
    -f, --data_format   - ssf, tnt, text
    -e, --encoding      - utf8, wx
    -i, --input_file    - path to the test data file
    -o, --output_file   - path to the output file
    
'''

import sys, os.path as path
sys.path.append(path.dirname(path.abspath(__file__)))

import tagger.src.data_reader as data_reader
import tagger.src.generate_features as generate_features
import tagger.utils.writer as data_writer
import tagger.src.evaluate as evaluate
import argparse
import logging
import pickle
import numpy as np
from time import time

import sklearn
import pycrfsuite


logger = logging.getLogger(__name__)


def get_args():
    ''' This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(description='Scorer pipeline')
    parser.add_argument("-p",'--pipeline_type', type=str, required=True,
                        help='Pipeline Type (train, test, predict)')
    parser.add_argument("-l", "--language", dest="language", type=str, metavar='<str>', required=True,
                         help="Language of the dataset: tel (telugu), hin (hindi), tam (tamil), kan (kannada), pun (pubjabi)")
    parser.add_argument("-t", "--tag_type", dest="tag_type", type=str, metavar='<str>', required=True,
                         help="Tag type: pos, chunk")
    parser.add_argument("-m", "--model_type", dest="model_type", type=str, metavar='<str>', default='regp',
                        help="Model type (crf|hmm|cnn|lstm:) (default=crf)")
    parser.add_argument("-e", "--encoding", dest="encoding", type=str, metavar='<str>',
                        help="Encoding of the data (utf8, wx)")
    parser.add_argument("-f", "--data_format", dest="data_format", type=str, metavar='<str>',
                        help="Data format (ssf, tnt, txt)")
    parser.add_argument("-i", "--input_file", dest="test_data", type=str, metavar='<str>', required=True,
                        help="Test data path ex: data/test/telugu/test.txt")
    parser.add_argument("-o", "--output_file", dest="output_path", type=str, metavar='<str>',
                         help="The path to the output file")


    return parser.parse_args()

def pipeline():
    curr_dir = path.dirname(path.abspath(__file__))
    args = get_args()


    model_path = "%s/models/%s/%s.%s.%s.crfsuite" % (curr_dir, args.language, args.model_type, args.tag_type, args.encoding)    

    if args.pipeline_type == 'train':
        logger.info('Start Training#')
        logger.info('Tagger model type: %s' % (args.model_type))
        train_data_path = "%s/data/train/%s/train.%s.%s" % (curr_dir, args.language, args.encoding, args.data_format)
        test_data_path = "%s/%s" % (curr_dir, args.test_data)      

        train_sents = data_reader.load_data(args.data_format, train_data_path, args.language)
        test_sents = data_reader.load_data(args.data_format, test_data_path, args.language)

        X_train = [ generate_features.sent2features(s, args.tag_type) for s in train_sents ]
        y_train = [ generate_features.sent2labels(s, args.tag_type) for s in train_sents ]

        X_test = [ generate_features.sent2features(s, args.tag_type) for s in test_sents ]
        y_test = [ generate_features.sent2labels(s, args.tag_type) for s in test_sents ]

        if args.model_type == "crf":

            trainer = pycrfsuite.Trainer(verbose=False)
            
            trainer.set_params({
            'c1': 1.0,   # coefficient for L1 penalty
            'c2': 1-3,  # coefficient for L2 penalty
            'max_iterations': 50,  # stop earlier

            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
            })

            for xseq, yseq in zip(X_train, y_train):
                trainer.append(xseq, yseq)

            trainer.train(model_path)

            tagger = pycrfsuite.Tagger()
            tagger.open(model_path)

            y_pred = [tagger.tag(xseq) for xseq in X_test]
            print(evaluate.bio_classification_report(y_test, y_pred))


    if args.pipeline_type == "test":
        test_data_path = "%s/%s" % (curr_dir, args.test_data)      

        test_sents = data_reader.load_data(args.data_format, test_data_path, args.language, tokenize_text=False)
        X_test = [ generate_features.sent2features(s, args.tag_type) for s in test_sents ]
        y_test = [ generate_features.sent2labels(s, args.tag_type) for s in test_sents ]

        if args.model_type == "crf":
            tagger = pycrfsuite.Tagger()
            tagger.open(model_path)

            y_pred = [tagger.tag(xseq) for xseq in X_test]
            print(evaluate.bio_classification_report(y_test, y_pred))

    if args.pipeline_type == "predict":

        test_data_path = "%s" % (args.test_data)      

        test_sents = data_reader.load_data(args.data_format, test_data_path, args.language, tokenize_text=True)
        X_test = [ generate_features.sent2features(s, args.tag_type) for s in test_sents ]

        if args.model_type == "crf":
            tagger = pycrfsuite.Tagger()
            tagger.open(model_path)

        y_pred = [tagger.tag(xseq) for xseq in X_test]

        output_file = "%s" % (args.output_path)
        data_writer.write_anno_to_file(output_file, test_sents, y_pred, args.tag_type)
        
if __name__ == '__main__':
    pipeline()
