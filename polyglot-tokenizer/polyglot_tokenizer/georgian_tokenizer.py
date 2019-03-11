#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import io
import os
import re

from .roman_tokenizer import RomanTokenizer


class GeorgianTokenizer(RomanTokenizer):
    def __init__(self, lang='ka', split_sen=False, smt=False):
        super(GeorgianTokenizer, self).__init__(lang='en', split_sen=split_sen, smt=smt, fit=False)
        self.georgian_alpha = ''.join([unichr(x) for x in range(0x10a0, 0x1100) if unichr(x).isalpha()])
        self.georgian_alpha += ''.join([unichr(x) for x in range(0x2d00, 0x2d30) if unichr(x).isalpha()])
        self.alpha += self.georgian_alpha
        self.alpha_lower += ''.join([x for x in self.georgian_alpha if x.islower()])
        self.alpha_upper += ''.join([x for x in self.georgian_alpha if x.isupper()])
        # compile regexes
        self.fit()
        # recompile regexes
        self.specascii = re.compile(r'([\\!@#$%^&*()_+={\[}\]|";:<>?`~/\u10fb\u2056])')
        if self.split_sen:
            self.splitsenr1 = re.compile(' ([.?]) ([%s])' % self.alpha_upper)
            self.splitsenr2 = re.compile(' ([.?]) ([\'"\(\{\[< ]+) '
                                         '([%s])' % self.alpha_upper)
            self.splitsenr3 = re.compile(
                ' ([.?]) ([\'"\)\}\]> ]+) ([%s])' % self.alpha_upper)
