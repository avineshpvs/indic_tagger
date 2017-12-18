'''
Pipeline code for Indic Tagger

Example:
python pipeline.py -p train -o outputs -l tel -t chunk -m crf -i data/test/tel/test.utf.conll.chunk -e utf -f conll

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
import argparse
import logging
import pickle
import numpy as np
from time import time
import sklearn
from tagger.src.algorithm.CRF import CRF

logger = logging.getLogger(__name__)


def get_args():
    ''' This function parses and return arguments passed in'''

    parser = argparse.ArgumentParser(description='Scorer pipeline')
    parser.add_argument("-p",'--pipeline_type', type=str, required=True,
                        help='Pipeline Type (train, test, predict)')
    parser.add_argument("-l", "--language", dest="language", type=str, metavar='<str>', required=True,
                         help="Language of the dataset: tel (telugu), hin (hindi), tam (tamil), kan (kannada), pun (pubjabi)")
    parser.add_argument("-t", "--tag_type", dest="tag_type", type=str, metavar='<str>', required=True,
                         help="Tag type: pos, chunk, parse")
    parser.add_argument("-m", "--model_type", dest="model_type", type=str, metavar='<str>', default='regp',
                        help="Model type (crf|hmm|cnn|lstm:) (default=crf)")
    parser.add_argument("-e", "--encoding", dest="encoding", type=str, metavar='<str>',
                        help="Encoding of the data (utf8, wx)")
    parser.add_argument("-f", "--data_format", dest="data_format", type=str, metavar='<str>',
                        help="Data format (ssf, tnt, txt)")
    parser.add_argument("-i", "--input_file", dest="test_data", type=str, metavar='<str>', required=True,
                        help="Test data path ex: data/test/telugu/test.txt")
    parser.add_argument("-o", "--output_file", dest="output_path", type=str, metavar='<str>',
                         help="The path to the output file",
                         default=path.join(path.dirname(path.abspath(__file__)), "outputs"))


    return parser.parse_args()

def pipeline():
    curr_dir = path.dirname(path.abspath(__file__))
    args = get_args()

    data_writer.set_logger(args.model_type, args.output_path)

    if args.tag_type != "parse":
        model_path = "%s/models/%s/%s.%s.%s.model" % (curr_dir, args.language, args.model_type, args.tag_type, args.encoding)    

    if args.pipeline_type == 'train':
        logger.info('Start Training#')
        logger.info('Tagger model type: %s' % (args.model_type))
        train_data_path = "%s/data/train/%s/train.%s.%s" % (curr_dir, args.language, args.encoding, args.data_format)
        test_data_path = "%s/%s" % (curr_dir, args.test_data)      

        train_sents = data_reader.load_data(args.data_format, train_data_path, args.language)
        test_sents = data_reader.load_data(args.data_format, test_data_path, args.language)

        X_train = [ generate_features.sent2features(s, args.tag_type, args.model_type) for s in train_sents ]
        y_train = [ generate_features.sent2labels(s, args.tag_type) for s in train_sents ]

        X_test = [ generate_features.sent2features(s, args.tag_type, args.model_type) for s in test_sents ]
        y_test = [ generate_features.sent2labels(s, args.tag_type) for s in test_sents ]

        print('Train data size:', len(X_train), len(y_train))
        print('Test data size:', len(X_test), len(y_test))


        if args.model_type == "crf":
            tagger = CRF(model_path)

        tagger.train(X_train, y_train)
        tagger.load_model()
        tagger.test(X_test, y_test)

    if args.pipeline_type == "test":
        test_data_path = "%s/%s" % (curr_dir, args.test_data)      

        test_sents = data_reader.load_data(args.data_format, test_data_path, args.language, tokenize_text=False)
        X_test = [ generate_features.sent2features(s, args.tag_type, args.model_type) for s in test_sents ]
        y_test = [ generate_features.sent2labels(s, args.tag_type) for s in test_sents ]

        if args.model_type == "crf":
            tagger = CRF(model_path)
            tagger.load_model()
            tagger.test(X_test, y_test)

    if args.pipeline_type == "predict":

        test_data_path = "%s" % (args.test_data)      
        test_sents = data_reader.load_data(args.data_format, test_data_path, args.language, tokenize_text=True)
        if args.tag_type == "parse":
            #Pos tagging
            X_test = [ generate_features.sent2features(s, "pos", args.model_type) for s in test_sents ]

            tag_model_path = "%s/models/%s/%s.%s.%s.model" % (curr_dir, args.language, args.model_type, "pos", args.encoding)  
            chunk_model_path = "%s/models/%s/%s.%s.%s.model" % (curr_dir, args.language, args.model_type, "chunk", args.encoding) 

            if args.model_type == "crf":
                tagger = CRF(tag_model_path)
                tagger.load_model()
                y_pos = tagger.predict(X_test)

                test_sents_pos = generate_features.append_tags(test_sents, "pos", y_pos)
                X_test = [ generate_features.sent2features(s, "chunk", args.model_type) for s in test_sents_pos ]

                chunker = CRF(chunk_model_path)
                chunker.load_model()
                y_chunk = chunker.predict(X_test)

                test_fname = path.basename(test_data_path)
                output_file = "%s/%s.parse" % (args.output_path, test_fname)
                data_writer.write_anno_to_file(output_file, test_sents_pos, y_chunk, "chunk")
                logger.info("Output: %s" % output_file)
                # data_writer.write_to_screen(output_file)
        else:            
            X_test = [ generate_features.sent2features(s, args.tag_type, args.model_type) for s in test_sents ]

            if args.model_type == "crf":
                tagger = CRF(model_path)
                tagger.load_model()
                y_pred = tagger.predict(X_test)

            output_file = "%s" % (args.output_path)
            data_writer.write_anno_to_file(output_file, test_sents, y_pred, args.tag_type)
        
if __name__ == '__main__':
    pipeline()
