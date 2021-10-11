

BIO  
B stands for 'beginning' (signifies beginning of an Named Entity, i.e. NE)  
I stands for 'inside' (signifies that the word is inside an NE)  
O stands for 'outside' (signifies that the word is just a regular word outside of an NE)  

2. BIOES  
B stands for 'beginning' (signifies beginning of an NE)  
I stands for 'inside' (signifies that the word is inside an NE)  
O stands for 'outside' (signifies that the word is just a regular word outside of an NE)  
E stands for 'end' (signifies that the word is the end of an NE)  
S stands for 'singleton'(signifies that the single word is an NE )  


**彭老师的代码，自己 debug 20 遍**  


现在能见到的 NLP 任务，基本上都能用 bert 解决。自己准备好数据，往里一丢就完事儿了。  

在把数据传入到神经网络之前都要先转换成向量，最后输出的向量转换成词。也就是说在数据在内部流动的时候，全部都是向量的形式。  

词向量模型，得到结果以后就不会再变了。但是用 self-attention 就可以根据不同的上下文语境，得到不同的词向量表示。  

把上下文的信息加入到当前词的词向量当中，通过加权的方式，这就是 self-attention。  

通过 Q、K、V 达到考虑上下文，找到可以表达词的特征的向量  

Q query 要去查询的（单个）  

K key 等着被查的（一串儿）  

V value 实际的特征信息  


a 权重，最开始就是根据词向量的内积算出来的，算出来之后又进行了 softmax  

分母中的根号是为了消除向量长度的影响，否则向量长度越长，值越大，这就影响了结果  

然后每一个词都算权重乘以 V，在求和，这样每一个词就都包含了全部上下文的信息。  

RNN 是一个词一个词算的，因为后面的词要等前面的词的结果。但是 attention 可以一批一批一起算。  

Multi-Head 就是 kernel，得到的是一个词的多种表达形式。  

最后的 feed forward 就是一个全连接网络，一是可以增加模型的能力，二是可以达到指定输出的维度。  

Multi-Head 最后的表现比较好，就是因为这种方法综合了多种特征表达。  

可以堆叠多层  

算 self-attention 的时候，损失了位置信息了，但是位置信息又是非常重要的，所以后面还要加上。  

加了残差连接  

在 decoder 端加入了 mask 机制，是因为比如机器翻译的时候，后面的词是要预测的值，如果不进行 mask 就相当于看到答案了。  

bert 用的就是 transformer 的 encoder，目的就是把词的特征找出来  

#### 训练 bert  

方法 1：  
句子中有 15% 的词被随机 mask 掉  

让模型去预测被 mask 掉的词是什么  

方法 2：  
预测两个句子是否应该连在一起  


#### 代码解读  

config.json 就是要训练的参数，比如 drop out 比例，lr 的值等等  

vocab.txt 就是所有的词  





