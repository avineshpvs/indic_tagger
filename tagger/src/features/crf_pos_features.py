def crf_pos_features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = [
        'bias',
        'word=' + word,                         #current word
        'word[-4:]=' + word[-4:],               #last 4 characters 
        'word[-3:]=' + word[-3:],               #last 3 characters
        'word[-2:]=' + word[-2:],               #last two characters
        'word.isdigit=%s' % word.isdigit(),     #is a digit
    ]
    if len(word) > 3:
        features.extend([
            'word.short=False'
        ])
    if len(word) < 3:
        features.extend([
            'word.short=True'
        ])
    if i > 0:
        word1 = sent[i-1][0]                                      
        features.extend([
            '-1:word=' + word1,                 #previous word
        ])
    else:
        features.append('BOS')
        
    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.extend([
            '+1:word=' + word1,                 #next word
        ])
    else:
        features.append('EOS')
                
    return features