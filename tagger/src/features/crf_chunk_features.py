def crf_chunk_features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word=' + word,                             #current word
        'word[-4:]=' + word[-4:],                   #last 4 characters 
        'word[-3:]=' + word[-3:],                   #last 3 characters
        'word[-2:]=' + word[-2:],                   #last 2 characters
        'word.isdigit=%s' % word.isdigit(),         #is a digit?
        'postag=' + postag,                         #current POS tag
        'postag[:2]=' + postag[:2],                 #first two characters of POS tag
    ]
    if len(word) > 3:
        features.extend([
            'word.short=False'
        ])
    if len(word) <= 3:
        features.extend([
            'word.short=True'
        ])
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.extend([
            '-1:word=' + word1,                     #previous word
            '-1:postag=' + postag1,                 #previous POS tag
            '-1:postag[:2]=' + postag1[:2],         #first two characters of previous POS tag
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word=' + word1,                     #next word
            '+1:postag=' + postag1,                 #next POS tag
            '+1:postag[:2]=' + postag1[:2],         #first two characters of next POS tag 
        ])
    else:
        features.append('EOS')
                
    return features