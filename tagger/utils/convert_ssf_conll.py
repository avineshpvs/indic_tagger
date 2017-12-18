import sys,os.path as path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

"""
Convert SSF To CONLL format

python convert_ssf_conll.py -i ../../data/test/tel/test.utf.ssf.pos -o ../../data/test/tel/test.utf.conll.pos

SSF format:
-----------

<Sentence id=1>
1	((	chunk11
1.1 word11	tag11
1.2	word12 	tag12		
	))
2	((	chunk12
2.1 word13 tag13
	))	
</Sentence>
<Sentence id=2>
1	((	chunk11
1.1 word11	tag11
1.2	word12 	tag12		
1.3 word13 tag13
	))	
</Sentence>
1 word11 tag11 B-chunk11
2 
3 word13 tag13 B-chunk13

CONLL format: (BI format)
-------------------------
1 word11 tag11 B-chunk11
2 word12 tag12 I-chunk11
3 word13 tag13 B-chunk12

1 word21 tag21 B-chunk21
2 word22 tag22 I-chunk22
3 word23 tag23 I-chunk23

"""

import re, os
import codecs
import logging
from tagger.src import data_reader
from tagger.utils.writer import write_to_file
import argparse
logger = logging.getLogger(__name__)

def convert_format(sents, filename):
	with codecs.open(filename, 'w', encoding='utf8', errors='ignore') as fp:
		for sent in sents:
			for index, item in enumerate(sent):
				fp.write(str(index+1) + "\t" + "\t".join(item) + "\n")
			fp.write("\n")

def get_args():
    ''' This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(description='Format Converter from SSF to CONLL')
    parser.add_argument("-i", "--input_path", dest="file_path", type=str, metavar='<str>', required=True,
                        help="File to be converted file path ex: data/test/telugu/test.wx.conll")
    parser.add_argument("-o", "--output_path", dest="output_path", type=str, metavar='<str>', required=True,
                         help="The path to the output file ex: outputs/test.utf.conll")
    return parser.parse_args()


if __name__ == "__main__":

	curr_dir = path.dirname(path.abspath(__file__))
	args = get_args()

	filename = "%s/%s" % (curr_dir, args.file_path)
	output_file = "%s/%s" % (curr_dir, args.output_path)
	sents = data_reader.load_data("ssf", filename, "")
	convert_format(sents, output_file)










