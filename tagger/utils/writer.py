
import codecs
import logging

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

def write_to_screen(filename):
    with codecs.open(filename, "r", encoding='utf8', errors='ignore') as fp:
        text = fp.read()
        print(text)
 
def mkdirp(path):
    if path == '':
        return
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def set_logger(method, out_dir=None):
    console_format = '[%(levelname)s] (%(name)s) %(message)s'
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(console_format))
    logger.addHandler(console)
    if out_dir:
        file_format = '[%(levelname)s] (%(name)s) %(message)s'
        log_file = logging.FileHandler(out_dir + '/%s.txt' % (method), mode='w')
        log_file.setLevel(logging.DEBUG)
        log_file.setFormatter(logging.Formatter(file_format))
        logger.addHandler(log_file)