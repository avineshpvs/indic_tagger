#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import io
import os
import re

from .roman_tokenizer import RomanTokenizer


class GreekTokenizer(RomanTokenizer):
    def __init__(self, lang='el', split_sen=False, smt=False):
        super(GreekTokenizer, self).__init__(lang=lang, split_sen=split_sen, smt=smt, fit=False)
        self.greek_alpha = ''.join([unichr(x) for x in range(0x0370, 0x0400) if unichr(x).isalpha()])
        self.greek_alpha += ''.join([unichr(x) for x in range(0x1f00, 0x2000) if unichr(x).isalpha()])
        self.alpha += self.greek_alpha
        self.alpha_lower += ''.join([x for x in self.greek_alpha if x.islower()])
        self.alpha_upper += ''.join([x for x in self.greek_alpha if x.isupper()])
        # compile regexes
        self.fit()
        # recompile regexes
        self.specascii = re.compile(r'([\\!@#$%^&*()_+={\[}\]|";:<>?`~/\u037e'
                                    r'\u1fbd-\u1fbf\u1fcd-\u1fcf\u1fdd-\u1fdf'
                                    r'\u1fed-\u1fef\u1ffd\u1ffe])')
        if self.split_sen:
            self.splitsenr1 = re.compile(' ([\u037e;.?]) ([%s])' % self.alpha_upper)
            self.splitsenr2 = re.compile(' ([\u037e;.?]) ([\'"\(\{\[< ]+) '
                                         '([%s])' % self.alpha_upper)
            self.splitsenr3 = re.compile(
                ' ([\u037e;.?]) ([\'"\)\}\]> ]+) ([%s])' % self.alpha_upper)
