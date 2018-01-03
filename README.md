# Indic Tagger

In this project, we build part-of-speech (POS) taggers and chunkers for Indian Languages.

Languages supported: Telugu, Hindi, Tamil, Marathi, Punjabi, Kannada, Malayalam, Urdu, Bengali

If you reuse this software, please use the following citation:

```
@inproceedings{PVS:SPSAL2007,
  editor    = {P.V.S., Avinesh and Gali, Karthik},
  title     = {Proceedings of the  Shallow Parsing for South Asian Languages (SPSAL) Workshop, held at IJCAI-07, Hyderabad, India},
  series    = {{SPSAL} Workshop Proceedings},
  month     = {January},
  year      = {2007},
  pages     = {21--24},
}
```

### Training Data Statistics and System Performances (F1 macro)

| Languages  |  # Words  | # Sents |  CRF POS    | CRF Chunk  |
| ---------- | ----------|---------|-------------|------------|
|   tel      |   347k    |   30k   |     93%     |    96%     |
|   hin      |   350k    |  16.3k  |     93%     |    97%     |
|   ben      |   298.3k  |  14.6k  |     84%     |    95%     |
|   pun      |   152.5k  |  5.6k   |     92%     |    98%     |
|   mar      |   207.9k  |  8.5k   |     89%     |    95%     |
|   urd      |   158.9k  |  7.6k   |     90%     |    96%     |
|   tam      |   337k    |  14.2k  |     88%     |    92%     |
|   mal      |   192k    |  11.4k  |             |    95%     | 
|   kan      |   294.3k  |  16.5k  |             |            |


### Install

	pip install -r requirements

	pip install git+git://github.com/irshadbhat/indic-tokenizer.git


### Run 

    python pipeline.py -p predict -l tel -t pos -m crf -f txt -e utf -i input_file -o output_file

    -l, --languages       select language (3 letter ISO-639 code) 
                          {hin, ben, mal, pun, tel, tam, kan, mar, urd}
    -t, --tag_type      	pos, chunk, parse
    -m, --model_type    	crf, hmm, cnn, lstm
    -f, --data_format   	ssf, tnt, txt, conll
    -e, --encoding      	utf8, wx   (default: utf8)
    -i, --input_file      <input-file>
    -o, --output_file     <output-file>
    -s, --sent_split      True/False (default: True)
	
    python pipeline.py --help 

    To Train:
    python pipeline.py -p train -o outputs -l tel -t pos -m crf -e utf -f ssf

### ToDo List

- [x] Telugu, Hindi trained CRF models
- [x] Bengali, Punjabi, Marathi, Urdu, Tamil trained CRF models
- [ ] Bug: Utf-8 error Malayalam, Kannada trained CRF models
- [ ] Bug: Punjabi & Urdu training file doesn't have "|" (or) end of sentence marker. 
- [ ] HMM trained  
- [ ] Maximum Entropy
- [ ] Deep learning (CNN, LSTM, BI-LSTM)
- [ ] Analysis Comparision w.r.t other ML algorithms



