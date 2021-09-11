
```python 
import http.client
import hashlib
import urllib
import random
import json
import time
import os,sys
import numpy as np
from LAC import LAC
from bert_serving.client import BertClient

def load_text(jsonfile):
    inf = open(jsonfile, 'r',errors='ignore')
    data = []
    for line in inf:
        #data.append({'sentence':line.strip()})
        data.append(line.strip())
    print('data load with %d records from %s'%( len(data), jsonfile))
    return data

class Text2Vec():
    def __init__(self):
        self.bc = BertClient()
        
        self.lac = LAC()
      
    def calc_sim(self, str1, str2):
        vec = self.bc.encode([str1,str2])
        #cacl similarity matrix
        cor = np.corrcoef(vec)
        return cor[0,1]

    def calc_sim_vec(self, a, m):
        """
        input:
            a ; a vector
            m ; a list of vector
        """
        c= np.sum(a*m, axis=1)/(np.linalg.norm(a)*np.linalg.norm(m,axis=1))
        return c
    
    def build_vec(self, text, outfile = ''):
        """
        text: [str1, str2...] n strings
        
        return:
            a np array shape (n, 768)
            save vec to outfile
        """
        if outfile and os.path.exists(outfile):
            return np.load(outfile)
                
        total_len = len(text)
        batch_size = 32
        sent_array = []
        #txtvec 
        for rowid in range(0, total_len, batch_size):
            sentences = []
            startid = rowid
            endid = rowid + batch_size
            if endid > total_len:
                endid = total_len

            for rid in range(startid, endid):
                retstr = text[rid]
                sentences.append(retstr)

            sent_array.append(sentences)

        #assert
        txtvec = ''
        cnt = 0
        for sents in sent_array:
            vec = self.bc.encode(sents)
            if isinstance(txtvec, str):
                txtvec = vec
            else:
                #print('vec.shape:', vec.shape)
                txtvec = np.concatenate([txtvec, vec], axis=0)

            cnt += 1    
            if cnt % 100 == 0:
                print('txtvec.shape:', txtvec.shape)

        print('txtvec.shape:', txtvec.shape)
        if outfile:
            np.save(outfile, txtvec)
        return txtvec

    def build_queryword_vec(self, queryword):
        queryword = [queryword]
        return self.bc.encode(queryword)
    
    def get_topKword(self, queryword, txtfile = '', topk=20):
        if txtfile == '':
            qword_file = queryword + '.txt'
        else:
            qword_file = txtfile
        if not os.path.exists(qword_file):
            print(f'Error, {qword_file} not exists, quit')
            return
    
        baiketxt = load_text(qword_file)
        result = self.lac.run(baiketxt)
        data = []
        for x in result:
            for w,pos in zip(x[0],x[1]):
                w = w.replace(' ','').lower()
                if len(w)>= 2 and pos and pos[0]=='n':
                    data.append(w)     
                    
#         data.append(queryword)
        data = set(sorted(data))
        data = sorted(data)
        allvec = self.build_vec(data, outfile=f'{qword_file}.vec.npy')
        queryword_vec = self.build_queryword_vec(queryword)
        
#         for id, x in enumerate(data):
#             if x == queryword:
#                 print(id, x) 
#                 break
            
#         rowid = id
#         print(data[rowid])
    
#         score = self.calc_sim_vec(allvec[rowid,:], allvec)
        score = self.calc_sim_vec(queryword_vec, allvec)
    
        #topk = 20
        topk_idx = np.argsort(score)[::-1][:topk]
        for idx in topk_idx:
            print('> %s\t%s' % (score[idx], data[idx]))      
```
