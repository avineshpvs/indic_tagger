# Indic Tagger

In this project, we build part-of-speech (POS) taggers and chunkers for Indian Languages.

Languages supported: Telugu, Hindi, Tamil, Marathi, Punjabi, Kannada, Malayalam

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

### Training Data Statistics and System Performances

| Languages  |  # Word   | # Sent  |  CRF POS    | CRF Chunk  |
| ---------- | ----------|---------|--------------------------|
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

	python tagger_pipeline.py -p predict -l tel -t pos -m crf -f text -e utf -i input_file -o output_file
	
    -l, --languages         select language (3 letter ISO-639 code) {hin,
                            ben, mal, pan, tel, tam, kan, mar}
    -t, --tag_type      	pos, chunk
    -m, --model_type    	crf, hmm, cnn, lstm
    -f, --data_format   	ssf, tnt, text
    -e, --encoding      	utf8, wx
    -i, --input_file        <input-file>
    -o, --output_file       <output-file>
	
	python tagger_pipeline.py --help 


### ToDo List

- [x] Telugu, Hindi trained CRF models
- [x] Bengali, Punjabi, Marathi, Urdu, Tamil trained CRF models
- [ ] Malayalam, Kannada trained CRF models
- [ ] HMM trained  
- [ ] Maximum Entropy
- [ ] Deep learning (CNN, LSTM, BI-LSTM)
- [ ] Analysis Comparision w.r.t other ML algorithms



