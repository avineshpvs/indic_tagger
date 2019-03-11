#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import io
import os
import re

from .roman_tokenizer import RomanTokenizer


class HebrewTokenizer(RomanTokenizer):
    def __init__(self, lang='he', split_sen=False, smt=False):
        super(HebrewTokenizer, self).__init__(lang=lang, split_sen=split_sen, smt=smt, fit=False)
        self.hebrew_alpha = ''.join([unichr(x) for x in range(0x0590, 0x0600) if unichr(x).isalpha()])
        self.alpha += self.hebrew_alpha
        self.alpha_lower += ''.join([x for x in self.hebrew_alpha if x.islower()])
        self.alpha_upper += ''.join([x for x in self.hebrew_alpha if x.isupper()])
        # compile regexes
        self.fit()
        # recompile regexes
        self.specascii = re.compile(r'([\\!@#$%^&*()_+={\[}\]|;:<>?`~/])')
        if self.split_sen:
            self.splitsenr1 = re.compile(' ([.?]) ([%s])' % self.alpha_upper)
            self.splitsenr2 = re.compile(' ([.?]) ([\'"\(\{\[< ]+) '
                                         '([%s])' % self.alpha_upper)
            self.splitsenr3 = re.compile(
                ' ([.?]) ([\'"\)\}\]> ]+) ([%s])' % self.alpha_upper)
