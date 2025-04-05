
import pycrfsuite
import tagger.src.evaluate as evaluate

class CRF():
	def __init__(self, model_path):
		self.trainer = pycrfsuite.Trainer(verbose=False)
		self.model_path = model_path
		self.trainer.set_params({
            'c1': 1.0,   # coefficient for L1 penalty
            'c2': 1-3,  # coefficient for L2 penalty
            'max_iterations': 50,  # stop earlier

            # include transitions that are possible, but not observed
            'feature.possible_transitions': True
            })

	def train(self, X_train, y_train):
		for xseq, yseq in zip(X_train, y_train):
			self.trainer.append(xseq, yseq)
		self.trainer.train(self.model_path)
	
import os

class CRF:
    # ... other methods ...

import os

class CRF:
    # ... other methods ...

    def load_model(self):
        self.model_dir = os.path.join(self.root, 'models', self.lang)
        # Assuming the model file is named 'model.bin' inside the directory
        self.model_path = os.path.join(self.model_dir, 'crf', self.tag_type, self.format + '.model', 'model.bin')
        try:
            self.tagger.open(self.model_path)
        except Exception as e:
            logging.error("Error loading CRF model: %s", e)
            raise
		
	def test(self, X_test, y_test):
		y_pred = self.predict(X_test)
		print(evaluate.bio_classification_report(y_test, y_pred))

	def predict(self, X_test):
		y_pred = [self.tagger.tag(xseq) for xseq in X_test]
		return y_pred




