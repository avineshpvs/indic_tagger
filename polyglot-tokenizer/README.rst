Tokenizer
=========

----

Tokenizer for world's most spoken languages and social media texts like Facebook, Twitter etc.


Install
^^^^^^^

::

    - git clone https://github.com/irshadbhat/polyglot-tokenizer.git
    - cd polyglot-tokenizer
    - sudo python setup.py install

Tokenizer
^^^^^^^^^

.. code:: python

    >>> from __future__ import unicode_literals
    >>> from polyglot_tokenizer import Tokenizer
    >>> tk = Tokenizer(lang='en', smt=True) #smt is a flag for social-media-text
    >>> text = "RT @BJP_RSS Crack down on Black money.India slides to 75th slot on Swiss bank money list #ModiForeignAchievements @RituRathaur https://t.c…"
    >>> tk.tokenize(text)
    ['RT', '@BJP_RSS', 'Crack', 'down', 'on', 'Black', 'money', '.', 'India', 'slides', 'to', '75th', 'slot', 'on', 'Swiss', 'bank', 'money', 'list', '#ModiForeignAchievements', '@RituRathaur', 'https://t.c…']
    >>> tk = Tokenizer(lang='hi')
    >>> tk.tokenize("22 साल के लंबे इंतजार के बाद आखिरकार हॉलीवुड स्टार लियोनार्डो डिकैप्रियो को अपनी पहली ऑस्कर ट्रॉफी"
    ...             " मिल चुकी है। उन्हें ये अवॉर्ड अपनी फिल्म ‘द रेवेनेंट’ में ह्यूज ग्लास के किरदार के लिए मिला, लेकिन उनके"
    ...             " के लिए रोल निभाना आसान नहीं था।")
    ['22', 'साल', 'के', 'लंबे', 'इंतजार', 'के', 'बाद', 'आखिरकार', 'हॉलीवुड', 'स्टार', 'लियोनार्डो', 'डिकैप्रियो', 'को', 'अपनी', 'पहली', 'ऑस्कर', 'ट्रॉफी', 'मिल', 'चुकी', 'है', '।', 'उन्हें', 'ये', 'अवॉर्ड', 'अपनी', 'फिल्म', "'", 'द', 'रेवेनेंट', "'", 'में', 'ह्यूज', 'ग्लास', 'के', 'किरदार', 'के', 'लिए', 'मिला', ',', 'लेकिन', 'उनके', 'के', 'लिए', 'रोल', 'निभाना', 'आसान', 'नहीं', 'था', '।']
    >>> tk = Tokenizer(lang='hi', split_sen=True)
    >>> tk.tokenize("22 साल के लंबे इंतजार के बाद आखिरकार हॉलीवुड स्टार लियोनार्डो डिकैप्रियो को अपनी पहली ऑस्कर ट्रॉफी"
    ...             " मिल चुकी है। उन्हें ये अवॉर्ड अपनी फिल्म ‘द रेवेनेंट’ में ह्यूज ग्लास के किरदार के लिए मिला, लेकिन उनके"
    ...             " के लिए रोल निभाना आसान नहीं था। फिल्म एक सीन के लिए लियोनार्डो को भैंस का कच्चा लीवर खाना"
    ...             " पड़ा था। जबकि असल जिंदगी में वो पूरी तरह शाकाहारी हैं। हालांकि इस सीन के लिए पहले लियोनार्डो को"
    ...             " मांस जैसे दिखने वाली चीज दी गई थी, लेकिन उन्हें लगा कि ऐसा करना गलत होगा। फिल्म के लिए इम्पोर्ट"
    ...             " की गई चीटियां...")
    [['22', 'साल', 'के', 'लंबे', 'इंतजार', 'के', 'बाद', 'आखिरकार', 'हॉलीवुड', 'स्टार', 'लियोनार्डो', 'डिकैप्रियो', 'को', 'अपनी', 'पहली', 'ऑस्कर', 'ट्रॉफी', 'मिल', 'चुकी', 'है', '।'], ['उन्हें', 'ये', 'अवॉर्ड', 'अपनी', 'फिल्म', "'", 'द', 'रेवेनेंट', "'", 'में', 'ह्यूज', 'ग्लास', 'के', 'किरदार', 'के', 'लिए', 'मिला', ',', 'लेकिन', 'उनके', 'के', 'लिए', 'रोल', 'निभाना', 'आसान', 'नहीं', 'था', '।'], ['फिल्म', 'एक', 'सीन', 'के', 'लिए', 'लियोनार्डो', 'को', 'भैंस', 'का', 'कच्चा', 'लीवर', 'खाना', 'पड़ा', 'था', '।'], ['जबकि', 'असल', 'जिंदगी', 'में', 'वो', 'पूरी', 'तरह', 'शाकाहारी', 'हैं', '।'], ['हालांकि', 'इस', 'सीन', 'के', 'लिए', 'पहले', 'लियोनार्डो', 'को', 'मांस', 'जैसे', 'दिखने', 'वाली', 'चीज', 'दी', 'गई', 'थी', ',', 'लेकिन', 'उन्हें', 'लगा', 'कि', 'ऐसा', 'करना', 'गलत', 'होगा', '।'], ['फिल्म', 'के', 'लिए', 'इम्पोर्ट', 'की', 'गई', 'चीटियां', '...']]

Tokenizer can also be called from Command Line Interface.

.. parsed-literal::

    irshad@polyglotnlp$ polyglot-tokenizer --h
    usage: polyglot-tokenizer [-h] [-v] [-i] [-s] [-t] [-o] [-l]
    
    Tokenizer for world's most spoken languages

    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -i , --input          <input-file>
      -s, --split-sentences
                            set this flag to apply sentence segmentation
      -t, --social-media-test
                            set this flag if the input file contains social media
                            text like twitter, facebook and whatsapp
      -o , --output         <output-file>
      -l , --language       select language (2 letter ISO-639 code) {hi, ur, bn,
                            as, gu, ml, pa, te, ta, kn, or, mr, cu, myv, nn, yi,
                            ne, bo, br, ks, en, es, ca, cs, de, el, en, fi, da,
                            eu, kok, nb, uz, fr, ga, hu, is, it, lt, lv, nl, pl,
                            pt, ro, ru, sk, bm, yue, mk, ku, sl, sv, zh, et, fo,
                            gl, hsb, af, ar, be, hy, bg, ka, ug, hr, mn, tk, kk,
                            ky, la, no, fa, uk, tl, tr, vi, yo, ko, got, ckb, he,
                            id, sr}


