import sys,os.path as path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

from tagger.src.features.crf_pos_features import crf_pos_features
from tagger.src.features.crf_chunk_features import crf_chunk_features
import numpy as np

def sent2features(sent, tag_type, model_type):
    if tag_type == "pos":
    	if model_type == "crf":
        	return [crf_pos_features(sent, i) for i in range(len(sent))]
    if tag_type == "chunk":
    	if model_type == "crf":
        	return [crf_chunk_features(sent, i) for i in range(len(sent))]

def sent2labels(sent, tag_type):
    if tag_type == "pos":
        return [postag for token, postag, chunk in sent]
    if tag_type == "chunk":
        return [chunk for token, postag, chunk in sent]

def sent2tokens(sent):
    return [token for token, postag, chunk in sent]


def append_tags(sents, tag_type, pred):
	#To do make it more efficient
	if tag_type == "pos":
		for i, sent in enumerate(sents):
			for j, vals in enumerate(sent): 
				if tag_type == "pos":
					sents[i][j][1] = pred[i][j]
				if tag_type == "chunk":
					sents[i][j][2] = pred[i][j]
	return sents

	"""

	np_sents = np.array(sents)
	if tag_type == "pos":
		np_sents[:,:,1] = np.array(pred)
	if tag_type == "chunk":
		np_sents[:,:,2] =  np.array(pred)

	return np_sents
	"""