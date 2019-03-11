#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import io
import os
import re

from .base import BaseTokenizer


class RomanTokenizer(BaseTokenizer):
    def __init__(self, lang='en', split_sen=False, smt=False, fit=True):
        super(RomanTokenizer, self).__init__(split_sen=split_sen, fit=False)
        self.tw = smt
        self.lang = lang
        ext = 'en' if lang == 'he' else lang
        file_path = os.path.dirname(os.path.abspath(__file__))
        with io.open('%s/data/nonbreaking_prefixes.%s' % (file_path, ext), encoding='utf-8') as fp:
            self.NBP = self.NBP | set(fp.read().split())
        # precompile regexes
        if fit:
            self.fit()

    def fit(self):
        self.base_fit()
        # seperate "," outside
        self.notanumc = re.compile('([^0-9]),')
        self.cnotanum = re.compile(',([^0-9])')
        # split contractions
        self.numcs = re.compile("([0-9])'s")
        self.naca = re.compile(
            "([^%s0-9])'([%s])" %((self.alpha,)*2))
        # split hyphens
        self.hypheninnun = re.compile('(-?[0-9]-+[0-9]-?){,}')
        self.ch_hyp_noalnum = re.compile('(.)-([^%s0-9])' %self.alpha)
        self.noalnum_hyp_ch = re.compile('([^%s0-9])-(.)' %self.alpha)
        # split sentences
        if self.split_sen:
            self.splitsenr1 = re.compile(' ([.?]) ([%s])' % self.alpha_upper)
            self.splitsenr2 = re.compile(' ([.?]) ([\'"\(\{\[< ]+) '
                                         '([%s])' % self.alpha_upper)
            self.splitsenr3 = re.compile(
                ' ([.?]) ([\'"\)\}\]> ]+) ([%s])' % self.alpha_upper)
        # split Latin lettrs followed by non-Latin letters and vice-versa
        #self.nonltn_ltn = re.compile('([^\u0000-\u024f])([\u0000-\u024f])')
        #self.ltn_nonltn = re.compile('([\u0000-\u024f])([^\u0000-\u024f])')
        if self.lang in ['fi', 'sv']:
            self.specascii = re.compile(r'([\\!@#$%^&*()_+={\[}\]|";<>?`~/])')
            self.split_colon = re.compile(r':([^%s])' %self.alpha_lower)

    def tokenize(self, text):
        # normalize unicode punctituation
        text = self.normalize_punkt(text)
        # mask emoticons and urls
        text = self.mask_emos_urls(text)
        # mask #tags and @ddresses
        if self.tw:
            text = self.mask_htag_uref(text)
            text = self.mask_rep_punct(text)
        # mask splitted contractions
        text = self.mask_sp_contractions(text)
        #text = self.nonltn_ltn.sub(r'\1 \2', text)
        #text = self.ltn_nonltn.sub(r'\1 \2', text)
        # split supplementary unicode
        text = self.bigu.sub(r' \1 ', text)
        # universal tokenization
        text = self.base_tokenize(text)
        if self.lang in ['fi', 'sv']:
            text = self.split_colon.sub(r' : \1', text)
        # seperate "," outside
        text = self.notanumc.sub(r'\1 , ', text)
        text = self.cnotanum.sub(r' , \1', text)
        # split contractions 
        text = self.nacna.sub(r"\1 ' \2", text)
        text = self.naca.sub(r"\1 ' \2", text)
        text = self.acna.sub(r"\1 ' \2", text)
        if self.lang in 'fr ga it ca pt ro sk sl'.split():
            text = self.aca.sub(r"\1' \2", text)
        elif self.lang == 'he':
            text = re.sub(r'([%s])"([^%s])' %((self.hebrew_alpha,)*2), r'\1 " \2', text)
            text = re.sub(r'([^%s])"([%s])' %((self.hebrew_alpha,)*2), r'\1 " \2', text)
            text = re.sub(r'([^%s])"([^%s])' %((self.hebrew_alpha,)*2), r'\1 " \2', text)
            text = re.sub(r"([a-zA-Z\u00c0-\u02b0])'([a-zA-Z\u00c0-\u02b0])", r"\1 '\2", text)
        else:
            text = self.aca.sub(r"\1 '\2", text)
        text = self.numcs.sub(r"\1 's", text)
        text = text.replace("''", " ' ' ")
        # split dots at word beginings
        text = re.sub(r' (\.+)([^0-9])', r' \1 \2', text)
        # seperate out hyphens
        text = self.multihyphen.sub(
            lambda m: r'%s' % (' '.join(m.group(1))),
            text)
        text = self.hypheninnun.sub(
            lambda m: r'%s' % (m.group().replace('-', ' - ')),
            text)
        text = self.ch_hyp_noalnum.sub(r'\1 - \2', text)
        text = self.noalnum_hyp_ch.sub(r'\1 - \2', text)
        # handle non-breaking prefixes
        text = self.tokenize_prefixes(text)
        # restore multi-dots
        text = self.restoredots.sub(lambda m: r'.%s' %
                                    ('.' * int((len(m.group(2)) / 3))),
                                    text)
        # unmask emoticons and urls
        text = self.unmask_emos_urls(text)
        # unmask splitted contractions
        text = self.unmask_sp_contractions(text)
        # unmask #tags and @ddress
        if self.tw:
            if self._ht_at:
                text = self.unmask_htag_uref(text)
            if self._rp_pt:
                text = self.unmask_rep_punct(text)
        # split sentences
        if self.split_sen:
            text = self.splitsenr1.sub(r' \1\n\2', text)
            text = self.splitsenr2.sub(r' \1\n\2 \3', text)
            text = self.splitsenr3.sub(r' \1 \2\n\3', text)
        if self.split_sen:
            return [sen.split() for sen in text.split('\n')]
        else:
            return text.split()
