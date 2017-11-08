import sys,os.path as path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

import re, os
import codecs
import logging
from irtokz import IndicTokenizer

logger = logging.getLogger(__name__)

def load_data(text_type, filename, lang, tokenize_text=False):
    data_tuple = []
    with codecs.open(filename, 'r', encoding='utf-8') as fp:
        logger.info('Loading text_type: %s data' % (text_type))
        if text_type == "ssf":
            start_c = -1
            for line in fp:
                line = line.strip()
                ds = line.split()
                #print ds
                if line == "":
                    continue
                elif line[0:2] == "<S":
                    sent = []
                elif line[0:3] == "</S":
                    data_tuple.append(sent)
                elif line[0] == "<":
                    continue
                elif ds[0] == "0" or ds[0] == "))":
                    continue
                elif ds[1] == "((":
                    start_c, chunk_tag = 1, ds[2]
                    #print "hello-chunk tag",chunk_tag
                elif ds[2]:
                    #print "--",line,"--"
                    word, tag = ds[1], ds[2]
                    if start_c == -1:
                        sent.append((word, tag, ""))
                    if start_c == 1:
                        sent.append((word, tag, "B-%s" % (chunk_tag)))
                        start_c = 0
                    if start_c == 0:
                        print(start_c)
                        sent.append((word, tag, "I-%s" % (chunk_tag)))
                    
        if text_type == "tnt":
            for line in fp:
                sent = []
                line = line.strip()
                ds = line.split()
                if line == "":
                    data_tuple.append(sent)
                    sent = []
                    if len(ds) == 1:
                        word, tag, chunk = ds[1], "",""
                    if len(ds) == 2:
                        word, tag, chunk = ds[1], ds[2], ""
                    if len(ds) == 3:
                        word, tag, chunk = ds[1], ds[2], ds[3]
                    sent.append([word, tag, chunk_tag])
            if sent:
                data_tuple.append(sent)

        if text_type == "text":
            for line in fp:
                sent = []
                if tokenize_text:
                    tok = IndicTokenizer(lang=lang, split_sen=False)
                    line = tok.tokenize(line)
                tokens = line.split()
                for token in tokens:
                    sent.append([token, "", ""])
                data_tuple.append(sent)

    return data_tuple

  