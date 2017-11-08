import sys,os.path as path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from tagger.src.pos_features import pos_features
from tagger.src.chunk_features import chunk_features

def sent2features(sent, tag_type):
    if tag_type == "pos":
        return [pos_features(sent, i) for i in range(len(sent))]
    if tag_type == "chunk":
        return [chunk_features(sent, i) for i in range(len(sent))]

def sent2labels(sent, tag_type):
    if tag_type == "pos":
        return [postag for token, postag, chunk in sent]
    if tag_type == "chunk":
        return [postag for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]