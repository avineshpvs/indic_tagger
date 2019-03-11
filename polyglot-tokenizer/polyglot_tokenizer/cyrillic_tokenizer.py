#!/usr/bin/env python
# -*- coding=utf-8 -*-

from __future__ import (division, unicode_literals)

import io
import os
import re

from .roman_tokenizer import RomanTokenizer


class CyrillicTokenizer(RomanTokenizer):
    def __init__(self, lang='be', split_sen=False, smt=False):
        super(CyrillicTokenizer, self).__init__(lang='en', split_sen=split_sen, smt=smt, fit=False)
        self.cyrillic_alpha = ''.join([unichr(x) for x in range(0x0400, 0x0530) if unichr(x).isalpha()])
        self.alpha += self.cyrillic_alpha
        self.alpha_lower += ''.join([x for x in self.cyrillic_alpha if x.islower()])
        self.alpha_upper += ''.join([x for x in self.cyrillic_alpha if x.isupper()])
        # compile regexes
        self.fit()
