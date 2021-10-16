
POS Part-of-speech tagging 词性标注  

BIO  
B stands for 'beginning' (signifies beginning of an Named Entity, i.e. NE)  
I stands for 'inside' (signifies that the word is inside an NE)  
O stands for 'outside' (signifies that the word is just a regular word outside of an NE)  

BIOES  
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







## bert 文章解读  

### 一、[BERT使用详解(实战)](https://www.jianshu.com/p/bfd0148b292e)  

BERT 模型，本质可以把其看做是新的 word2Vec。对于现有的任务，只需把 BERT 的输出看做是 word2vec，在其之上建立自己的模型即可了。  

\#  type_ids: 0     0  0    0    0     0       0 0     1  1  1  1   1 1  
\# 这里 "type_ids" 主要用于区分第一个第二个句子。  

tokenizer：是 bert 源码中提供的模块，其实主要作用就是将句子拆分成字，并且将字映射成 id  

bert 模型对输入的句子有一个最大长度  


### 二、[Bert系列（一）——demo运行](https://www.jianshu.com/p/3d0bb34c488a)  

学习一个开源项目，第一步是安装，第二步是跑下demo，第三步才是阅读源码。  

安装 bert 简单，直接 github 上拉下来就可以了，跑 demo 其实也不难，参照 README.md 一步步操作就行了。  

1、下载bert源码：直接 clone。git clone https://github.com/google-research/bert.git  

2、下载预训练模型  

cased 表示区分大小写，uncased 表示不区分大小写。  

3、下载训练数据  

MRPC 文件，要科学上网才能下载。解决办法是手动下载，注释掉代码里的下载文件的内容。命令里指定文件夹目录为自己放下载文件的目录。    

4、run demo  

设置环境变量，指定预训练模型文件和语料地址  

```shell
export BERT_BASE_DIR=/path/to/bert/uncased_L-12_H-768_A-12
export GLUE_DIR=/path/to/glue_data
```

在 bert 源码文件里执行 run_classifier.py，基于预训练模型进行 fine-tune  

```shell
python run_classifier.py \
  --task_name=MRPC \
  --do_train=true \
  --do_eval=true \
  --data_dir=$GLUE_DIR/MRPC \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$BERT_BASE_DIR/bert_model.ckpt \
  --max_seq_length=128 \
  --train_batch_size=32 \
  --learning_rate=2e-5 \
  --num_train_epochs=3.0 \
  --output_dir=/tmp/mrpc_output/
```

预测：指定fine-tune之后模型文件所在地址  

```shell
export TRAINED_CLASSIFIER=/path/to/fine/tuned/classifier  
```

执行以下语句完成预测任务，预测结果输出在 output_dir 文件夹中  

```shell
python run_classifier.py \
  --task_name=MRPC \
  --do_predict=true \
  --data_dir=$GLUE_DIR/MRPC \
  --vocab_file=$BERT_BASE_DIR/vocab.txt \
  --bert_config_file=$BERT_BASE_DIR/bert_config.json \
  --init_checkpoint=$TRAINED_CLASSIFIER \
  --max_seq_length=128 \
  --output_dir=/tmp/mrpc_output/
```

### 三、[Bert系列（二）——源码解读之模型主体](https://www.jianshu.com/p/d7ce41b58801)  

modeling.py  

class BertConfig(object) 模型配置  

输入的 from_tensor 当作 query，to_tensor 当作 key 和 value。当 self attention 的时候 from_tensor 和 to_tensor 是同一个值。  

（1）bert 主要流程是先 embedding（包括位置和 token_type 的 embedding），然后调用 transformer 得到输出结果，其中 embedding、embedding_table、所有 transformer 层输出、最后 transformer 层输出以及 pooled_output 都可以获得，用于迁移学习的 fine-tune 和预测任务；  

（2）bert 对于 transformer 的使用仅限于 encoder，没有 decoder 的过程。这是因为模型存粹是为了预训练服务，而预训练是通过语言模型，不同于 NLP 其他特定任务。在做迁移学习时可以自行添加；  

### 四、[Bert系列（四）——源码解读之Fine-tune](https://www.jianshu.com/p/116bfdb9119a)  

重要的是明白根据不同任务调整输入格式和对 loss 的构建，这两个知识点学会之后，基本上也可以依葫芦画瓢做一些自己的任务了。  

bert 官方给了两个任务的 fine-tune 代码:  

1.run_classifier.py  
2.run_squad.py  

参数都比较简单。有两个要注意。  

max_seq_length：指定 WordPiece tokenization 之后的 sequence 的最大长度，要求小于等于预训练模型的最大 sequence 长度。当输入的数据长度小于 max_seq_length 时用 0 补齐，如果长度大于 max_seq_length 则 truncate 处理；  

warmup_proportion：warm up 步数的比例，比如说总共学习 100 步，warmup_proportion=0.1 表示前 10 步用来 warm up，warm up 时以较低的学习率进行学习(lr=global_step/num_warmup_steps * init_lr)，10 步之后以正常(或衰减)的学习率来学习。  

guid 是该样本的唯一 ID，text_a 和 text_b 表示句子对，lable 表示句子对关系，如果是 test 数据集则 label 统一为 0。    


### 五、[使用 Bert 预训练模型文本分类](https://www.jiqizhixin.com/articles/2019-03-13-4)  

![bert](https://image.jiqizhixin.com/uploads/editor/7e4af9e0-e178-40f3-b9c9-4d8ef46e99e9/640.png)  

**对于文本分类任务，一个句子中的 N 个字符对应了 E_1, …, E_N，这 N 个 embedding。文本分类实际上是将 BERT 得到的 T_1 这一层连接上一个全连接层进行多分类。**  

数据格式：  

game    APEX 是个新出的吃鸡游戏。  
technology  Google 将要推出 tensorflow2.0。  

一行代表一个文本，由标签加上一个tab加上正文组成。  

将文本分割为三个文件，train.tsv(训练集)，dev.tsv(验证集)，test.tsv(测试集)；然后放置在同一个data_dir文件夹下。  

run_classfier.py 参数：DATA_DIR 是训练数据所在的文件夹，BERT_BASE_DIR 是 bert 预训练模型位置。task_name 要和 DataProcessor 类中的名称一致。do_train 是否 fine tune，do_eval 是否 evaluation，do_predict 是否预测。如果不需要 fine tune，或显卡配置太低，可以将 do_trian 去掉。max_seq_length 代表了句子的最长长度，当显存不足时，可以适当降低 max_seq_length。  

以句子向量的形式使用 Bert：如果想要将 bert 模型的编码和其他模型一起使用，将 bert 模型作为句子向量使用很有意义（也就是所谓的句子级别的编码）。可以使用 bert-as-service。安装完 bert-as-service，就可以用 bert 模型将句子映射到固定长度的向量上。  


### 六、[全面解读 bert](https://www.jiqizhixin.com/articles/2018-11-01-9)  

各种 NLP 任务只需要少量数据进行微调就能实现非常好的效果  

1、简介  

BERT 的核心过程非常简洁，它会先从数据集抽取两个句子，其中第二句是第一句的下一句的概率是 50%，这样就能学习句子之间的关系。  

其次随机去除两个句子中的一些词，并要求模型预测这些词是什么，这样就能学习句子内部的关系。  

最后再将经过处理的句子传入大型 Transformer 模型，并通过两个损失函数同时学习上面两个目标就能完成训练。  


极大数据集上进行预训练对于不同的 NLP 任务都会有帮助。  

Transformer，其实越大的数据量就越能显示出这个结构的优点，因为它可以叠加非常深的层级。  

项目作者表示一般使用 Uncased 模型就可以了，除非大小写对于任务很重要才会使用 Cased 版本。  

每一个文件都包含了三部分，即保存预训练模型与权重的 ckpt 文件、将 WordPiece 映射到单词 id 的 vocab 文件，以及指定模型超参数的 json 文件。  

2、Transformer 概览  

在整个 Transformer 架构中，它只使用了注意力机制和全连接层来处理文本，因此 Transformer 确实没使用循环神经网络或卷积神经网络实现「特征抽取」这一功能。此外，Transformer 中最重要的就是自注意力机制，这种在序列内部执行 Attention 的方法可以视为搜索序列内部的隐藏关系，这种内部关系对于翻译以及序列任务的性能有显著提升。  

如 Seq2Seq 一样，原版 Transformer 也采用了编码器-解码器框架。  

点乘注意力是注意力机制的一般表达形式，将多个点乘注意力叠加在一起可以组成 Transformer 中最重要的 Multi-Head Attention 模块，多个 Multi-Head Attention 模块堆叠在一起就组成了 Transformer 的主体结构，并借此抽取文本中的信息。  

经过 SoftMax 函数后可得出一组归一化的概率。这些概率相当于给源语输入序列做加权平均，即表示在生成一个目标语单词时源语序列中哪些词是重要的。  

Multi-head Attention 其实就是多个点乘注意力并行处理并将最后的结果拼接在一起。这种注意力允许模型联合关注不同位置的不同表征子空间信息，我们可以理解为在参数不共享的情况下，多次执行点乘注意力。  

3、BERT 论文解读  

BERT 的全称是基于 Transformer 的双向编码器表征，其中「双向」表示模型在处理某一个词时，它能同时利用前面的词和后面的词两部分信息。这种「双向」的来源在于 BERT 与传统语言模型不同，它不是在给定所有前面词的条件下预测最可能的当前词，而是随机遮掩一些词，并利用所有没被遮掩的词进行预测。  

BERT 最核心的过程就是同时预测加了 MASK 的缺失词与 A/B 句之间的二元关系  

![bert input](https://image.jiqizhixin.com/uploads/editor/f313e8ea-a022-4109-a95d-d6686f82b350/1541060383093.png)  

如上所示，输入有 A 句「my dog is cute」和 B 句「he likes playing」这两个自然句，我们首先需要将每个单词及特殊符号都转化为词嵌入向量，因为神经网络只能进行数值计算。其中特殊符 [SEP] 是用于分割两个句子的符号，前面半句会加上分割编码 A，后半句会加上分割编码 B。  

因为要建模句子之间的关系，BERT 有一个任务是预测 B 句是不是 A 句后面的一句话，而这个分类任务会借助 A/B 句最前面的特殊符 [CLS] 实现，该特殊符可以视为汇集了整个输入序列的表征。  

为了令 Transformer 感知词与词之间的位置关系，我们需要使用位置编码给每个词加上位置信息。  

BERT 最核心的就是预训练过程，简单而言，模型会从数据集抽取两句话，其中 B 句有 50% 的概率是 A 句的下一句，然后将这两句话转化前面所示的输入表征。现在我们随机遮掩（Mask 掉）输入序列中 15% 的词，并要求 Transformer 预测这些被遮掩的词，以及 B 句是 A 句下一句的概率这两个任务。  

![bert pre-training](https://image.jiqizhixin.com/uploads/editor/57b4f6ac-8542-4c1d-9533-e83d5ff9cc15/1541060382808.png)  

首先谷歌使用了 BooksCorpus（8 亿词量）和他们自己抽取的 Wikipedia（25 亿词量）数据集，每次迭代会抽取 256 个序列（A+B），一个序列的长度为小于等于 512 个「词」。因此 A 句加 B 句大概是 512 个词，每一个「句子」都是非常长的一段话，这和一般我们所说的句子是不一样的。这样算来，每次迭代模型都会处理 12.8 万词。(256 X 512)  

对于二分类任务，在抽取一个序列（A+B）中，B 有 50% 的概率是 A 的下一句。如果是的话就会生成标注「IsNext」，不是的话就会生成标注「NotNext」，这些标注可以作为二元分类任务判断模型预测的凭证。  

对于 Mask 预测任务，首先整个序列会随机 Mask 掉 15% 的词，这里的 Mask 不只是简单地用「[MASK]」符号代替某些词，因为这会引起预训练与微调两阶段不是太匹配。所以谷歌在确定需要 Mask 掉的词后，80% 的情况下会直接替代为「[MASK]」，10% 的情况会替代为其它任意的词，最后 10% 的情况会保留原词。  

原句：my dog is hairy  

80%：my dog is [MASK]  

10%：my dog is apple  

10%：my dog is hairy  

最后预训练完模型，就要尝试把它们应用到各种 NLP 任务中，并进行简单的微调。不同的任务在微调上有一些差别，但 BERT 已经强大到能为大多数 NLP 任务提供高效的信息抽取功能。对于分类问题而言，例如预测 A/B 句是不是问答对、预测单句是不是语法正确等，它们可以直接利用特殊符 [CLS] 所输出的向量 C，即 P = softmax(C * W)，新任务只需要微调权重矩阵 W 就可以了。  

对于其它序列标注或生成任务，我们也可以使用 BERT 对应的输出信息作出预测。下图展示了 BERT 在任务中的微调方法，它们都只添加了一个额外的输出层。在下图中，Tok(Token) 表示不同的词、E 表示输入的嵌入向量、T_i 表示第 i 个词在经过 BERT 处理后输出的上下文向量。  

![bert fine tune](https://image.jiqizhixin.com/uploads/editor/e61ee732-66e4-4961-83bb-34a08654e354/1541060383644.png)

如上图所示，句子级的分类问题只需要使用对应 [CLS] 的 C 向量，例如（a）中判断问答对是不是包含正确回答的 QNLI、判断两句话有多少相似性的 STS-B 等，它们都用于处理句子之间的关系。句子级的分类还包含（b）中判语句中断情感趋向的 SST-2 和判断语法正确性的 CoLA 任务，它们都是处理句子内部的关系。  

在 SQuAD v1.1 问答数据集中，研究者将问题和包含回答的段落分别作为 A 句与 B 句，并输入到 BERT 中。通过 B 句的输出向量，模型能预测出正确答案的位置与长度。最后在命名实体识别数据集 CoNLL 中，每一个 Tok 对应的输出向量 T 都会预测它的标注是什么，例如人物或地点等。  


### 七、[BERT介绍](https://blog.csdn.net/triplemeng/article/details/83053419)  
















































