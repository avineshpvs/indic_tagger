
import codecs
def write_to_file(text, filename):
    with codecs.open(filename, 'w', encoding='utf8', errors='ignore') as fp:
    	fp.write(text)


def write_anno_to_file(filename, X_data, y_data, tag_type):
	with codecs.open(filename, 'w', encoding='utf8', errors='ignore') as fp:
		text = ""
		for i, X_sent in enumerate(X_data):
			fp.write("<s>\n")
			for j, X_token in enumerate(X_sent):
				if tag_type == "pos":
					X_token[1] = y_data[i][j]
				if tag_type == "chunk":
					X_token[2] = y_data[i][j]
				fp.write("%s\n" % "\t".join(X_token))
			fp.write("</s>\n")