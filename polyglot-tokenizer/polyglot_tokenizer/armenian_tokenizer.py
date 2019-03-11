#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import io
import os
import re

from .roman_tokenizer import RomanTokenizer


class ArmenianTokenizer(RomanTokenizer):
    def __init__(self, lang='hy', split_sen=False, smt=False):
        super(ArmenianTokenizer, self).__init__(lang='en', split_sen=split_sen, smt=smt, fit=False)
        self.armenian_alpha = ''.join([unichr(x) for x in range(0x0530, 0x0590) if unichr(x).isalpha()])
        self.alpha += self.armenian_alpha
        self.alpha_lower += ''.join([x for x in self.armenian_alpha if x.islower()])
        self.alpha_upper += ''.join([x for x in self.armenian_alpha if x.isupper()])
        # compile regexes
        self.fit()
        # recompile regexes
        self.specascii = re.compile(r'([\\!@#$%^&*()_+={\[}\]|";:<>?`~/\u0559-\u055c\u0589])')
        if self.split_sen:
            self.splitsenr1 = re.compile(' ([\u0589:.?]) ([%s])' % self.alpha_upper)
            self.splitsenr2 = re.compile(' ([\u0589:.?]) ([\'"\(\{\[< ]+) '
                                         '([%s])' % self.alpha_upper)
            self.splitsenr3 = re.compile(
                ' ([\u0589:.?]) ([\'"\)\}\]> ]+) ([%s])' % self.alpha_upper)
