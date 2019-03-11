#!/usr/bin/env python

from .indic_tokenizer import IndicTokenizer
from .roman_tokenizer import RomanTokenizer
from .greek_tokenizer import GreekTokenizer
from .hebrew_tokenizer import HebrewTokenizer
from .armenian_tokenizer import ArmenianTokenizer
from .cyrillic_tokenizer import CyrillicTokenizer
from .georgian_tokenizer import GeorgianTokenizer


class Tokenizer():
    def __init__(self, lang='en', split_sen=False,
                 smt=False, from_file=False):
        self.from_file = from_file
        self.split_sen = split_sen
        if lang in 'hsb da fo no nn'.split():
            lang = 'de'
        elif lang in ['et']:
            lang = 'fi'
        elif lang in ['gl', 'la']:
            lang = 'it'
        elif lang in 'af bm eu br tl tr vi yo ko hr id got'.split():
            lang = 'en'
        elif lang in 'ar ckb fa ug uz ku tk'.split():
            lang = 'ur'
        if lang in 'hi ur bn as gu ml pa te ta kn or mr ne bo kok ks'.split():
            self.tok = IndicTokenizer(lang=lang, split_sen=split_sen,
                                      smt=smt)
        elif lang in 'be bg cu kk ky ru uk sr mk mn myv'.split():
            self.tok = CyrillicTokenizer(lang=lang, split_sen=split_sen,
                                      smt=smt)
        elif lang == 'hy':
            self.tok = ArmenianTokenizer(lang=lang, split_sen=split_sen,
                                      smt=smt)
        elif lang == 'ka':
            self.tok = GeorgianTokenizer(lang=lang, split_sen=split_sen,
                                      smt=smt)
        elif lang == 'el':
            self.tok = GreekTokenizer(lang=lang, split_sen=split_sen,
                                      smt=smt)
        elif lang in 'he yi'.split():
            self.tok = HebrewTokenizer(lang=lang, split_sen=split_sen,
                                      smt=smt)
        else:
            self.tok = RomanTokenizer(lang=lang, split_sen=split_sen,
                                      smt=smt)

    def tokenize(self, sentence):
        if self.from_file or not self.split_sen:
            return self.tok.tokenize(sentence)
        else:
            out_sents = []
            sentences = sentence.split('\n')
            for sent in sentences:
                tok_sent = self.tok.tokenize(sent)
                out_sents.extend(tok_sent)
            return out_sents
