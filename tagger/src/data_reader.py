import re, os
import codecs
import logging
from irtokz import IndicTokenizer

logger = logging.getLogger(__name__)

def load_data(text_type, filename, lang, tokenize_text=False, split_sent=True):
    data_tuple = []
    with codecs.open(filename, 'r', encoding='utf-8') as fp:
        logger.info('Loading text_type: %s format' % (text_type))
        if text_type == "ssf":
            start_c = -1
            for line in fp:
                line = line.strip()
                ds = line.split()
                print("Line", line)
                print("DS", ds)
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
                        sent.append((word, tag, "I-%s" % (chunk_tag)))          
        elif text_type == "conll":
            sent = []
            for line in fp:
                line = line.strip()
                ds = line.split()
                if line != "":
                    if len(ds) == 2:
                        word, tag, chunk = ds[1], "",""
                    if len(ds) == 3:
                        word, tag, chunk = ds[1], ds[2], ""
                    if len(ds) == 4:
                        word, tag, chunk = ds[1], ds[2], ds[3]
                    sent.append([word, tag, chunk])
                else:
                    data_tuple.append(sent)
                    sent = []
        elif text_type == "txt":
            if split_sent == True:
                text = fp.read()
                tok = IndicTokenizer(lang=lang, split_sen=False)
                tokenize_sents = tok.tokenize(text)
                for line in tokenize_sents:
                    sent = []
                    tokens = line.split()
                    for token in tokens:
                        sent.append([token, "", ""])
                    data_tuple.append(sent)
            else:
                for line in fp:
                    sent = []
                    if tokenize_text:
                        tok = IndicTokenizer(lang=lang, split_sen=False)
                        line = tok.tokenize(line)
                    tokens = line.split()
                    for token in tokens:
                        sent.append([token, "", ""])
                    data_tuple.append(sent)
        else:
            print("Check - text_type", text_type)

    return data_tuple