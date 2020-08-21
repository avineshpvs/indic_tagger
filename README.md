# Indic Tagger (Indian Language Tagger)

In this project, we build part-of-speech (POS) taggers and chunkers for Indian Languages.

Languages supported: Telugu (te), Hindi (hi), Tamil (ta), Marathi (mr), Punjabi (pa), Kannada (kn), Malayalam (ml), Urdu (ur), Bengali (bn)

If you reuse this software, please use the following citation:

```
@inproceedings{PVS:SPSAL2007,
  editor    = {P.V.S., Avinesh and Gali, Karthik},
  title     = {Part of Speech Tagging and Chunking using Conditional Random Fields and Transformation Based Learning}
  booktitle = {Proceedings of the  Shallow Parsing for South Asian Languages (SPSAL) Workshop, held at IJCAI-07, Hyderabad, India},
  series    = {{SPSAL} Workshop Proceedings},
  month     = {January},
  year      = {2007},
  pages     = {21--24},
}
```

### Training Data Statistics and System Performances (F1 macro)

| Languages  |  # Words  | # Sents |  CRF POS    | CRF Chunk  | BI-LSTM-CRF POS  |  BI-LSTM CRF Chunk |
| ---------- | ----------|---------|-------------|------------|------------------|--------------------|
|   te       |   347k    |   30k   |     93%     |    96%     |  92%             |         92%        |
|   hi       |   350k    |  16.3k  |     93%     |    97%     |  **94%**         |         93%        |
|   bn       |   298.3k  |  14.6k  |     84%     |    95%     |  **85%**         |         88%        |
|   pa       |   152.5k  |  5.6k   |     92%     |    98%     |  **94%**         |         96%        |
|   mr       |   207.9k  |  8.5k   |     89%     |    95%     |  88%             |         90%        |
|   ur       |   158.9k  |  7.6k   |     90%     |    96%     |  **92%**         |         89%        |
|   ta       |   337k    |  14.2k  |     88%     |    92%     |  87%             |         85%        |
|   ml       |   192k    |  11.4k  |     96%     |    95%     |  **98%**         |         98%        |
|   kn       |   294.3k  |  16.5k  |     90%     |    98%     |  88%             |         87%        |


### Training Data Statistics and System Performances (F1 macro) for NER

| Languages  |  # Words  | # Sents |  CRF NER    | BI-LSTM-CRF NER  | 
| ---------- | ----------|---------|-------------|------------|
|   te       |   347k    |   30k   |     69%     |   65%      |
|   hi       |   503k    |   19k |    62%      |    63%     |
|   bn       |   120k    |   6k  |    54%      |     48%    |
|   ur       |   35k    |    1.5k |   65%       |    56%     |
|   or       |    93k   |   1.8k |    68%      |     43%    |

### Install using Anaconda

```
    # INSTALL python environment
    conda create -n tagger3.6 anaconda python=3.6
    source activate tagger3.6
    
    # Install the tokenizer
    cd polyglot-tokenizer
    python setup.py install
    
    # Install requirements
    pip install -r requirements.txt
```

### Run 
```
    python pipeline.py -p predict -l te -t pos -m crf -f txt -e utf -i input_file -o output_file

    -l, --languages       select language (2 letter ISO-639 code) 
                          {hi, be, ml, pu, te, ta, ka, mr, ur}
    -t, --tag_type      	pos, chunk, parse, ner
    -m, --model_type    	crf, hmm, lstm
    -f, --data_format   	ssf, txt, conll
    -e, --encoding      	utf8, wx   (default: utf8)
    -i, --input_file      <input-file>
    -o, --output_file     <output-file>
    -s, --sent_split      True/False (default: True)
	
    python pipeline.py --help 
```

Train the POS tagger:
   
```
    # CRF model
    python pipeline.py -p train -o outputs -l te -t pos -m crf -e utf -f ssf
    
    # BI-LSTM-CRF model
    python pipeline.py -p train -t pos -f conll -m lstm -e utf -l te
```

Predict on text:
    
```
    # CRF models 
    python pipeline.py -p predict -l te -t pos -m crf -f txt -e utf -i data/test/te/test.utf.txt
    
    # BI-LSTM-CRF models
    python pipeline.py -p predict -l te -t pos -m lstm -f txt -e utf -i data/test/te/test.utf.txt
    
    # SpaCy models
    python spacy_tagger_test.py -l te -t pos
```
  
  

Train the NER tagger:
   
```
    # CRF model
    python pipeline.py -p train -o outputs -l te -t ner -m crf -e utf -f conll
    
    # BI-LSTM-CRF model
    python pipeline.py -p train -t ner -f conll -m lstm -e utf -l te
```

Predict NER on text:
   
```
    # CRF model
    python pipeline.py -p predict -l hi -t ner -m crf -f txt -e utf -i data/test/hi/test.utf.txt
    
    # BI-LSTM-CRF model
    python pipeline.py -p predict -l hi -t ner -m lstm -f txt -e utf -i data/test/hi/test.utf.txt
```

### ToDo List

- [x] Telugu, Hindi trained CRF models
- [x] Bengali, Punjabi, Marathi, Urdu, Tamil trained CRF models
- [x] Bug: Utf-8 error Malayalam, Kannada trained CRF models
- [x] Deep learning (BI-LSTM-CRF)
- [x] Analysis Comparision w.r.t other ML algorithms
- [ ] Bug: Punjabi & Urdu training file doesn't have "|" (or) end of sentence marker. 
- [ ] NER for Indian Languages
- [ ] Feature addition to BI-LSTM-CRF models
- [ ] Active Learning based sampling strategies

