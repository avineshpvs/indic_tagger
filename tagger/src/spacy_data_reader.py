import re, os
import codecs
import logging
from irtokz import IndicTokenizer

logger = logging.getLogger(__name__)

def spacy_load_data(filename):
    file = open(filename, "r")
    sentence = ""
    posList = list()
    wordList = list()
    fullList = list()
    for line in file.readlines():
        if (line.strip() == ""):
            dict = {}
            dict['tags'] = posList
            dict['words'] = wordList
            tuple1 = (sentence.strip(), dict)
            fullList.append(tuple1)
            sentence = ""
            posList = list()
            wordList = list()
        else:
            array = re.split('\s+', line.strip())
            if (array[1] != "" and array[2] != ""):
                sentence = sentence + array[1] + " "
                posList.append(array[2])
                wordList.append(array[1])
    return fullList
