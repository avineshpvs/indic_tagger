#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import io
import re
import os
import string

try:
    unichr
except NameError:
    unichr = chr

class BaseTokenizer(object):

    def __init__(self, split_sen=False, fit=True):
        self.split_sen = split_sen
        file_path = os.path.dirname(os.path.abspath(__file__))
        # Internet Domains (most frequent ones)
        with io.open('%s/data/DOMAINS' % file_path, encoding='utf-8') as fp:
            self.domains = set(fp.read().split())
        # List of Emoticons
        with io.open('%s/data/EMOTICONS' % file_path, encoding='utf-8') as fp:
            self.emoticons = set(fp.read().split())
        # List of Non-breaking Prefixes
        with io.open('%s/data/nonbreaking_prefixes.en' % file_path, encoding='utf-8') as fp:
            self.NBP = set(fp.read().split())
        self.punctuation = set(string.punctuation)
        self.pemos = set([x for x in self.emoticons if
            (any(c in self.punctuation for c in x) and all(ord(c)<256 for c in x))])
        self.NBP = self.NBP.union(set(string.ascii_letters[:26]))
        self.NBP_NUM = set(['No', 'no', 'Art', 'pp'])
        self.contractions = """ 'all 'am 'clock 'd 'll 'm n't
                            're 's 'sup 'tis 'twas 've 'n' """
        self.contractions = self.contractions.split() +\
            self.contractions.upper().split()
        self.alpha = ''.join([unichr(x) for x in range(0x0000, 0x02b0) if unichr(x).isalpha()])
        self.alpha += ''.join([unichr(x) for x in range(0x1e00, 0x1f00) if unichr(x).isalpha()])
        self.alpha_lower = ''.join([x for x in self.alpha if x.islower()])
        self.alpha_upper = ''.join([x for x in self.alpha if x.isupper()])
        if fit:
            # precompile regexes
            self.base_fit()

    def base_fit(self):
        # ASCII junk characters
        self.ascii_junk = re.compile('[\x00-\x1f]')
        # Latin-1 supplementary characters
        self.latin = re.compile('([\xa1-\xbf\xd7\xf7])')
        # Latin-1 lowercase
        self.latin = re.compile('([\xa1-\xbf\xd7\xf7])')
        # general unicode punctuations except "’"
        self.uv_punct = re.compile('([\u2012-\u2018\u201a-\u206f])')
        # unicode mathematical operators
        self.umathop = re.compile('([\u2200-\u2211\u2213-\u22ff])')
        # unicode fractions
        self.ufrac = re.compile('([\u2150-\u2160])')
        # unicode superscripts and subscripts
        self.usupsub = re.compile('([\u2070-\u209f])')
        # unicode currency symbols
        self.ucurrency = re.compile('([\u20a0-\u20cf])')
        # all "other" ASCII special characters
        self.specascii = re.compile(r'([\\!@#$%^&*()_+={\[}\]|";:<>?`~/])')
        # keep multiple dots together
        self.multidot = re.compile(r'(\.\.+)([^\.])')
        # seperate "," outside
        self.notanumc = re.compile('([^0-9]),')
        self.cnotanum = re.compile(',([^0-9])')
        # split contractions
        self.rnb = re.compile("([a-zA-Z])('[nN]')([a-zA-Z])")
        self.ntc = re.compile("([a-zA-Z'])([nN]'[tT])([a-zA-Z' ])")
        self.numcs = re.compile("([0-9])'s")
        self.aca = re.compile(
            "([%s])'([%s])" % ((self.alpha,)*2))
        self.acna = re.compile(
            "([%s])'([^%s])" % ((self.alpha,)*2))
        self.nacna = re.compile(
            "([^%s])'([^%s])" % ((self.alpha,)*2))
        # split hyphens
        self.multihyphen = re.compile('(-+)')
        # restore multi-dots
        self.restoredots = re.compile(r'(DOT)(\1*)MULTI')
        # split supplementary unicode
        try:
            self.bigu = re.compile('([\U00010000-\U0010ffff]+)')
        except re.error:
            # UCS-2 build
            self.bigu = re.compile(u'(([\uD800-\uDBFF][\uDC00-\uDFFF])+)')
        self.isurl = re.compile(r'[a-z][a-z][.][a-z][a-z]').search
        self.joints = re.compile(r'(^[A-Za-z][A-Za-z]+)[.]'
                                 r'([A-Za-z][A-Za-z]+$)')
        self.rpunct = re.compile(r'[.,\\!@#$%^&\'*()_+={\[}\]|";:<>?`~/]')
        self.rep_punkt = re.compile(r'([%s][%s]+)' % (('.,\\!@#$%^&*()_+={\[}\]|;:<>?~/-',) * 2))
        self.rep_quotes = re.compile(r'([\'"`][\'"`]+)')

    def unmask_htag_uref(self, text):
        text = text.split()
        for i, token in enumerate(text):
            if token.startswith('hAsHtAg-'):
                ht_id = int(token.split('-')[1])
                text[i] = self.htag_dict[ht_id]
            elif token.startswith('uSeRrEf-'):
                uref_id = int(token.split('-')[1])
                text[i] = self.uref_dict[uref_id]
        return ' '.join(text)

    def mask_htag_uref(self, text):
        self.htag_dict = dict()
        self.uref_dict = dict()
        text = text.split()
        n_h = 0
        n_u = 0
        for i, token in enumerate(text):
            if token[0] == '#':
                text[i] = 'hAsHtAg-%d' % n_h
                self.htag_dict[n_h] = token
                n_h += 1
            elif token[0] == '@':
                text[i] = 'uSeRrEf-%d' % n_u
                self.uref_dict[n_u] = token
                n_u += 1
        self._ht_at = False
        if n_h or n_u:
            self._ht_at = True
        return ' '.join(text)

    def unmask_rep_punct(self, text):
        text = text.split()
        for i, token in enumerate(text):
            if token.startswith('rEpPuNcT-'):
                rp_id = int(token.split('-')[1])
                text[i] = self.punc_dict[rp_id]
        return ' '.join(text)

    def mask_rep_punct(self, text):
        n_p = 0
        self.punc_dict = dict()
        text = self.rep_quotes.sub(r' \1 ', text)
        text = self.rep_punkt.sub(r' \1 ', text)
        text = text.split()
        for i, token in enumerate(text):
            if self.rep_punkt.match(token) or self.rep_quotes.match(token):
                text[i] = 'rEpPuNcT-%d' % n_p
                self.punc_dict[n_p] = token
                n_p += 1
        self._rp_pt = False
        if n_p:
            self._rp_pt = True
        return ' '.join(text)

    def unmask_sp_contractions(self, text):
        text = ' %s ' % text
        for i, cn in enumerate(self.contractions):
            text = text.replace(' cOnTrAcTiOn-%d ' % i, ' %s ' % cn)
        return text

    def mask_sp_contractions(self, text):
        text = ' %s ' % text
        text = self.ntc.sub(r"\1 \2 \3", text)
        text = self.rnb.sub(r"\1 \2 \3", text)
        for i, cn in enumerate(self.contractions):
            text = text.replace(' %s ' % cn, ' cOnTrAcTiOn-%d ' % i)
        return text

    def normalize_punkt(self, text):
        """replace unicode punctuation by ascii"""
        text = re.sub('[\u2010\u2043]', '-', text)  # hyphen
        text = re.sub('[\u2018\u2019]', "'", text)  # single quotes
        text = re.sub('[\u201c\u201d]', '"', text)  # double quotes
        return text

    def unmask_emos_urls(self, text):
        text = text.split()
        for i, token in enumerate(text):
            if token.startswith('eMoTiCoN-'):
                emo_id = int(token.split('-')[1])
                text[i] = self.emos_dict[emo_id]
            elif token.startswith('sItEuRl-'):
                url_id = int(token.split('-')[1])
                text[i] = self.url_dict[url_id]
                #text[i] = 'U-R-L'
        return ' '.join(text)

    def mask_emos_urls(self, text):
        n_e, n_u = 0, 0
        text = re.sub(r'([\W_])(http://|https://|www.)', r'\1 \2', text)
        if self.tw:
            words = text.split()
            text = []
            for wd in words:
                if len(wd) > 2 and any(c in self.punctuation for c in wd):
                    for em in self.pemos:
                        br = len(em)
                        if len(wd) <= br:
                            continue
                        if wd.startswith(em) and (not (wd[br].isalpha() and em[-1].isalpha()))\
                                and (not (wd[br].isdigit() and em[-1].isdigit())):
                            wd = '%s %s' %(wd[:br], wd[br:])
                        if wd.endswith(em) and (not (wd[-br-1].isalpha() and em[0].isalpha()))\
                                and (not (wd[-br-1].isdigit() and em[0].isdigit())):
                            wd = '%s %s' %(wd[:-br], wd[-br:])
                text.append(wd)
            text = ' '.join(text).split()
        else:
            text = text.split()
        self.url_dict = dict()
        self.emos_dict = dict()
        for i, token in enumerate(text):
            if token in self.emoticons:
                text[i] = 'eMoTiCoN-%d' % n_e
                self.emos_dict[n_e] = token
                n_e += 1
                continue
            is_url = False
            if (token.startswith('http://') or
                token.startswith('https://') or
                    token.startswith('www.')):
                is_url = True
            elif self.isurl(token):
                tokens = self.rpunct.split(token)
                is_url = any(x in self.domains for x in tokens[1:])
            if is_url:
                t2 = ''
                if token[-2:] == "'s":
                    t2 = "'s"
                    token = token[:-2]
                elif token[-1] in ",.!?;:'\"":
                    t2 = token[-1]
                    token = token[:-1]
                text[i] = 'sItEuRl-%d' % n_u
                self.url_dict[n_u] = '%s %s' % (token, t2)
                n_u += 1
                continue
        text = ' '.join(text)
        text = ' %s ' % (text)
        return text

    def tokenize_prefixes(self, text):
        words = text.split()
        text_len = len(words) - 1
        text = str()
        for i, word in enumerate(words):
            if word[-1] == '.':
                dotless = word[:-1]
                if dotless.isdigit() and dotless not in self.NBP:
                    word = dotless + ' .'
                elif (('.' in dotless and re.search('[%s]' %self.alpha, dotless)) or
                        dotless in self.NBP):
                    pass
                elif (dotless in self.NBP_NUM and
                      (i < text_len and words[i + 1][0].isdigit())):
                    pass
                #elif i < text_len and words[i + 1][0].isdigit():
                #    pass
                else:
                    word = dotless + ' .'
            elif self.joints.search(word):
                w1, w2 = word.split('.')
                if word in self.NBP:
                    pass
                elif w1 in self.NBP:
                    word = '%s. %s' % (w1, w2)
                else:
                    word = '%s . %s' % (w1, w2)
            text += "%s " % word
        return ' %s ' % text

    def base_tokenize(self, text):
        text = ' %s ' % (text)
        # seperate out on Latin-1 supplementary characters
        text = self.latin.sub(r' \1 ', text)
        # seperate out on general unicode punctuations except "’"
        text = self.uv_punct.sub(r' \1 ', text)
        # seperate out on unicode mathematical operators
        text = self.umathop.sub(r' \1 ', text)
        # seperate out on unicode fractions
        text = self.ufrac.sub(r' \1 ', text)
        # seperate out on unicode superscripts and subscripts
        text = self.usupsub.sub(r' \1 ', text)
        # seperate out on unicode currency symbols
        text = self.ucurrency.sub(r' \1 ', text)
        # remove ascii junk
        text = self.ascii_junk.sub('', text)
        # seperate out all "other" ASCII special characters
        text = self.specascii.sub(r' \1 ', text)
        # keep multiple dots together
        text = self.multidot.sub(lambda m: r' %sMULTI %s' % (
            'DOT' * len(m.group(1)), m.group(2)), text)
        return text
