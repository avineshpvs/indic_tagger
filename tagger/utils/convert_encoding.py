import sys,os.path as path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))

"""
Convert WX to UTF

To run:
python tagger/utils/convert_encoding.py -ie wx -oe utf -d ssf -f data/train/hin/train.wx.ssf -o outputs/train.utf.ssf -l hin

-ie - Input encoding
-oe - Output encoding
-d -  Data format (ssf)
-i -  Input file
-o -  Output file
"""

import re, os
import codecs
import logging
from wxconv import WXC
from tagger.utils.writer import write_to_file
import argparse
logger = logging.getLogger(__name__)

def convert_encoding(filename, text_type, language, in_enc, out_enc):

	with codecs.open(filename, 'r', encoding='utf-8') as fp:
		logger.info('Loading text_type: %s data' % (text_type))
		output_data = ""
		if text_type == "ssf":
			converter = WXC(order='%s2%s' % (in_enc, out_enc), lang=language)
			for line in fp:
				line = line.strip()
				ds = line.split()
				#print("Line:--", ds)
				if line == "":
					output_data += u"\n"
				elif line[0] == "<":
					output_data += u"%s\n" % (line)
				elif ds[0] == "))":
					output_data += u"\t%s\n" % (line)
				elif ds[0] == "0" or ds[1] == "((":
					output_data += u"%s\n" % (u"\t".join(ds))
				elif ds[1] != "":
					#print("check", ds)
					word, tag = ds[1], ds[2]
					word_con = converter.convert(word)
					output_data += u"%s\t%s\t%s\n" % (ds[0], word_con, tag)
				else:
					pass
			return output_data
		else:
			if text_type == "tnt":
				converter = WXC(order='%s2%s' % (in_enc, out_enc), lang=language, format_='tnt')
			elif text_type == "text":
				converter = WXC(order='%s2%s' % (in_enc, out_enc), lang=language)
			elif text_type == "conll":
				converter = WXC(order='%s2%s' % (in_enc, out_enc), lang=language, format_='conll')
			else:
				raise Exception("Unknown Format %s" % text_type)
				pass
       		text = fp.read()
        	output_data = converter.convert(text)
       		return output_data

def get_args():
    ''' This function parses and return arguments passed in'''
    parser = argparse.ArgumentParser(description='Encoding Converter for Indian Languages')
    parser.add_argument("-l", "--language", dest="language", type=str, metavar='<str>', required=True,
                         help="Language of the dataset: tel (telugu), hin (hindi), tam (tamil), kan (kannada), pun (pubjabi)")
    parser.add_argument("-ie", "--in_enc", dest="in_enc", type=str, metavar='<str>', required=True,
                        help="Input Encoding of the data (utf, wx)")
    parser.add_argument("-oe", "--out_enc", dest="out_enc", type=str, metavar='<str>', required=True,
                        help="Input Encoding of the data (utf, wx)")
    parser.add_argument("-d", "--data_format", dest="data_format", type=str, metavar='<str>', required=True,
                        help="Data format (ssf, tnt, txt)")
    parser.add_argument("-i", "--input_path", dest="file_path", type=str, metavar='<str>', required=True,
                        help="File to be converted file path ex: data/test/telugu/test.wx.ssf")
    parser.add_argument("-o", "--output_path", dest="output_path", type=str, metavar='<str>', required=True,
                         help="The path to the output file ex: outputs/test.utf.ssf")

    return parser.parse_args()


if __name__ == "__main__":

	args = get_args()

	output_data=convert_encoding(args.input_path, args.data_format, args.language, args.in_enc, args.out_enc)
	write_to_file(output_data, args.output_path)










