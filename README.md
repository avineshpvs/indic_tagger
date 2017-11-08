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

- [x] Telugu, Hindi utf, wx trained CRF
- [ ] Bengali, Marathi, Punjabi,  utf, wx trained CRF
- [ ] HMM trained  
- [ ] Maximum Entropy
- [ ] Deep learning (CNN, LSTM, BI-LSTM)
- [ ] Analysis Comparision w.r.t other ML algorithms



