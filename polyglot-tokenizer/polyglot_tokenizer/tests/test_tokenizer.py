#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from testtools import TestCase
from tokenizer import Tokenizer, parse_args, process_args


class TestTokenizer(TestCase):
    def setUp(self):
        super(TestTokenizer, self).setUp()
        self.languages = "eng hin urd ben guj mal pan tel tam kan ori".split()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))

    def test_tokenizer(self):
        for lang in self.languages:
            tok = Tokenizer(split_sen=True, lang=lang)
            with io.open('%s/%s.txt' % (self.test_dir, lang),
                         encoding='utf-8') as fp:
                for line in fp:
                    tokenized_text = tok.tokenize(line)
                    # Dummy Assertion
                    self.assertIsInstance(tokenized_text, list)

    def test_parser(self):
        # test parser arguments
        parser = parse_args(['--input', 'path/to/input_file',
                             '--output', 'path/to/output_file',
                             '--language', 'kas',
                             '--split-sentences'])
        self.assertEqual(parser.infile, 'path/to/input_file')
        self.assertEqual(parser.outfile, 'path/to/output_file')
        self.assertEqual(parser.lang, 'kas')
        self.assertTrue(parser.split_sen)
        # test parser args processing
        process_args(parse_args(['-i', '%s/eng.txt' % self.test_dir,
                                 '-o', '/tmp/test.out',
                                 '-l', 'eng',
                                 '-s']))
