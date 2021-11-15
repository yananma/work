
```python 
def normalize_dataset(dataset, MAXLEN=128):
    """
    replace sentence by abstract if it is too long
    
    """
    newdata = []
    for rec in dataset.data:
        if rec['keyword'] not in rec['sentence'] and rec['brand'] not in rec['sentence']:
            continue
        else:
            if len(rec['sentence']) >= MAXLEN:
                keyword, brand = rec['keyword'], rec['brand']
                sentence_list = rec['sentence'].split('...') 
                rec['sentence'] = '...'.join([sent for sent in sentence_list if keyword in sent or brand in sent])
                maxlen_sentence = rec['sentence'][:MAXLEN]
                if keyword in maxlen_sentence or brand in maxlen_sentence:
                    rec['sentence'] = maxlen_sentence
                else:
                    if keyword in rec['sentence']:
                        pos = rec['sentence'].find(keyword) 
                        start = rec['sentence'][pos-64:pos] 
                        end = rec['sentence'][pos:pos+64] 
                        rec['sentence'] = start + end
                    elif brand in rec['sentence']:
                        pos = rec['sentence'].find(brand) 
                        start = rec['sentence'][pos-64:pos] 
                        end = rec['sentence'][pos:pos+64] 
                        rec['sentence'] = start + end
                newdata.append(rec)
            else:
                newdata.append(rec)
    
    dataset.data = newdata
    return dataset
```


