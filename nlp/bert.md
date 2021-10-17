
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

加了残差连接(因为有残差连接，所以可以堆叠很多层)  

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

#### 1、简介  

BERT 的核心过程非常简洁，它会先从数据集抽取两个句子，其中第二句是第一句的下一句的概率是 50%，这样就能学习句子之间的关系。  

其次随机去除两个句子中的一些词，并要求模型预测这些词是什么，这样就能学习句子内部的关系。  

最后再将经过处理的句子传入大型 Transformer 模型，并通过两个损失函数同时学习上面两个目标就能完成训练。  


极大数据集上进行预训练对于不同的 NLP 任务都会有帮助。  

Transformer，其实越大的数据量就越能显示出这个结构的优点，因为它可以叠加非常深的层级。  

项目作者表示一般使用 Uncased 模型就可以了，除非大小写对于任务很重要才会使用 Cased 版本。  

每一个文件都包含了三部分，即保存预训练模型与权重的 ckpt 文件、将 WordPiece 映射到单词 id 的 vocab 文件，以及指定模型超参数的 json 文件。  

#### 2、Transformer 概览  

在整个 Transformer 架构中，它只使用了注意力机制和全连接层来处理文本，因此 Transformer 确实没使用循环神经网络或卷积神经网络实现「特征抽取」这一功能。此外，Transformer 中最重要的就是自注意力机制，这种在序列内部执行 Attention 的方法可以视为搜索序列内部的隐藏关系，这种内部关系对于翻译以及序列任务的性能有显著提升。  

如 Seq2Seq 一样，原版 Transformer 也采用了编码器-解码器框架。  

点乘注意力是注意力机制的一般表达形式，将多个点乘注意力叠加在一起可以组成 Transformer 中最重要的 Multi-Head Attention 模块，多个 Multi-Head Attention 模块堆叠在一起就组成了 Transformer 的主体结构，并借此抽取文本中的信息。  

经过 SoftMax 函数后可得出一组归一化的概率。这些概率相当于给源语输入序列做加权平均，即表示在生成一个目标语单词时源语序列中哪些词是重要的。  

Multi-head Attention 其实就是多个点乘注意力并行处理并将最后的结果拼接在一起。这种注意力允许模型联合关注不同位置的不同表征子空间信息，我们可以理解为在参数不共享的情况下，多次执行点乘注意力。  

#### 3、BERT 论文解读  

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

BERT 做了两项改进：  

采取新的预训练的目标函数：the “masked language model” (MLM) 随机 mask 输入中的一些 tokens，然后在预训练中对它们进行预测。这样做的好处是学习到的表征能够融合两个方向上的 context。这个做法非常像 skip-gram。过去的同类算法在这里有所欠缺，比如 ELMo，它用的是两个单向的 LSTM 然后把结果拼接起来；还有 OpenAI GPT，虽然它一样使用了 transformer，但是只利用了一个方向的注意力机制，本质上也一样是单项的语言模型。  

增加句子级别的任务：“next sentence prediction”。作者认为很多 NLP 任务比如 QA 和 NLI 都需要对两个句子之间关系的理解，而语言模型不能很好的直接产生这种理解。为了理解句子关系，作者同时 pre-train 了一个 “next sentence prediction” 任务。具体做法是随机替换一些句子，然后利用上一句进行 IsNext/NotNext 的预测。  

在实际的预训练中，这两个任务是 jointly training。  

BERT BASE：L=12, H=768, A=12, Total Parameters=110M  
BERT LARGE：L=24, H=1024, A=16, Total Parameters=340M  
L 是 layers 层数(即 Transformer blocks 个数)，H 是 hidden vector size, A 是 self-attention 的 head 数(因为 h 表示 hidden 了)。  

每句话的第一个 token 总是 [CLS]。对应它的最终的 hidden state(即 Transformer 的输出)用来表征整个句子，可以用于下游的分类任务。  

模型能够处理句子对。为区别两个句子，用一个特殊 token [SEP] 隔开它们，另外针对不同的句子，把学习到的 Segment embeddings 加到每个 token 的 embedding 上  

单个句子仅使用一个 Segment embedding  

Masked LM：为了达到真正的 bidirectional 的 LM 的效果，作者创新性地提出了 Masked LM，但是缺点是如果常常把一些词 mask 起来，未来的 fine tuning 过程中模型有可能没见过这些词。这个量积累下来还是很大的。因为作者在他的实现中随机选择了句子中 15% 的 WordPiece tokens 作为要 mask 的词。  

Next Sentence Prediction：很多 NLP 的任务比如 QA 和 NLI 都需要理解两个句子之间的关系，而语言模型并不能直接反应这种关系。为了是预训练出来的模型很好的适应这些任务，作者提出了这样的一个预训练任务。实验表明，增加这样的一个任务在针对下游的 QA 和 NLI 任务时效果非常好。   

对于句子级的分类任务，BERT 的微调方法非常直观。论文用 [CLS] 来对应整个句子的表征。我们只需要把它作为输入通过一层网络，最后做 softmax 就可以了。  

GLUE 是一个自然语言任务集合。  

General Language Understanding Evaluation  


### 八、[BERT 源码分析及使用方法](https://cloud.tencent.com/developer/article/1454853)  

BERT是一种能够生成句子中词向量表示以及句子向量表示的深度学习模型，其生成的向量表示可以用于词级别的自然语言处理任务（如序列标注）和句子级别的任务（如文本分类）。  

input_ids（句子中词 id 组成的 tensor）到 sequence_output（句子中每个词的向量表示） pooled_output（句子的向量表示）  

BertConfig 类包含了一个 BertModel 所需的超参数  

vocab 词表  

is_training：如果训练则填 true，否则填 false，该参数会决定是否执行 dropout。    

先按照 token_type_id（即输入的句子中各个词语的 type，如对两个句子的分类任务，用 type_id 区分第一个句子还是第二个句子）    

输入的 input_mask（即与句子真实长度匹配的 mask，如 batch_size 为 2，句子实际长度分别为 2，3，则 mask 为 [[1, 1, 0], [1, 1, 1]]）  


### 九、[使用 BERT 进行词嵌入](https://www.infoq.cn/article/QK7zfPgQPCmZyITumZNG)  

BERT 模型使用大型句子语料库进行预训练。简而言之，训练是通过在一个句子中对一些单词进行掩码（大约为 15% 的单词），然后让模型去预测那些被掩码的单词。随着模型的预测训练，它学会了生成一个强大的单词内部表示，即词嵌入（Word embedding）。  

Bert-as-a-service 是一个 Python 库，它使我们能够在本地机器上部署预训练 BERT 模型并运行推理。它可以用于服务任何已发布的模型类型，也可以服务于针对特定下游任务进行微调的模型。  

### 十、[bert 算法介绍](https://www.itcast.cn/news/20200907/13593265501.shtml)  

BERT 采用了 Transformer Encoder block 进行连接(就当成是 LSTM 就行，本质上是一样的)  

词嵌入向量: word embeddings  

语句分块向量: segmentation embeddings  

位置编码向量: position embeddings  

最终的 embedding 向量是将上述的 3 个向量直接做加和的结果。  

Transformer Encoder 在训练的过程中, 并不知道它将要预测哪些单词，哪些单词是原始的， 哪些单词被遮掩成了[MASK]，哪些单词被替换成了其他单词。正是在这样一种高度不确定的情况下, 逼着模型学习该 token 的分布式上下文的语义, 尽最大努力学习原始语言说话的样子。同时因为原始文本中只有 15% 的 token 参与了 MASK 操作, 并不会破坏原语言的表达能力和语言规则。  

整个 Bert 在 11 项语言模型大赛中，基本思路就是双向 Transformer 负责提取特征，然后整个网络加一个全连接线性层作为 fine-tuning 微调。就是傻瓜式操作。  


### 十一、[理解 BERT 模型](https://baijiahao.baidu.com/s?id=1651912822853865814&wfr=spider&for=pc)  

Masked LM，在句子中随机遮盖一部分单词，然后同时利用上下文的信息预测遮盖的单词，这样可以更好地根据全文理解单词的意思。Masked LM 是 BERT 的重点。  

Next Sentence Prediction (NSP)，下一句预测任务，这个任务主要是让模型能够更好地理解句子间的关系。  

![bert pre-train and fine-tune](https://pics6.baidu.com/feed/574e9258d109b3dee994cc84f0bfb484800a4c3c.png?token=a8fb7222089a0143d0c3aaff2dc37b79&s=F980CB1A8FE4491B4EC0ADC8030090B3)  

左侧的图表示了预训练的过程，右边的图是对于具体任务的微调过程。  

BERT 的输入可以包含一个句子对 (句子 A 和句子 B)，也可以是单个句子。  

[CLS] 标志放在第一个句子的首位，经过 BERT 得到的的表征向量 C 可以用于后续的分类任务。  
[SEP] 标志用于分开两个输入句子，例如输入句子 A 和 B，要在句子 A，B 后面增加 [SEP] 标志。  
[MASK] 标志用于遮盖句子中的一些单词，将单词用 [MASK] 遮盖之后，再利用 BERT 输出的 [MASK] 向量预测单词是什么。  

例如给定两个句子 "my dog is cute" 和 "he likes palying" 作为输入样本，BERT 会转为 "[CLS] my dog is cute [SEP] he likes play ##ing [SEP]"。BERT 里面用了 WordPiece 方法，会将单词拆成子词单元 (SubWord)，所以有的词会拆出词根，例如 "palying" 会变成 "paly" + "##ing"。  

BERT 得到要输入的句子后，要将句子的单词转成 Embedding，Embedding 用 E表示。BERT 的输入 Embedding 由三个部分相加得到：Token Embedding，Segment Embedding，Position Embedding。  

Token Embedding：单词的 Embedding，例如 [CLS] dog 等，通过训练学习得到。  

Segment Embedding：用于区分每一个单词属于句子 A 还是句子 B，如果只输入一个句子就只使用 EA，通过训练学习得到。  

Position Embedding：编码单词出现的位置，与 Transformer 使用固定的公式计算不同，BERT 的 Position Embedding 也是通过学习得到的，在 BERT 中，假设句子最长为 512。  

![bert pre-train](https://pics6.baidu.com/feed/728da9773912b31b4e5f008cbd18ee7fdab4e16f.png?token=11ad868c3006ac5573d77892b3720d49&s=1FA07D2383DE55C81EEC0DC20200E0B2)  

预训练得到的 BERT 模型可以在后续用于具体 NLP 任务的时候进行微调 (Fine-tuning 阶段)，BERT 模型可以适用于多种不同的 NLP 任务，如下图所示。  

![nlp tasks](https://camo.githubusercontent.com/db8527714875965eb7c2120534b2580cab1092d3d0fc05ec373a58fc88ca7e30/68747470733a2f2f696d6167652e6a6971697a686978696e2e636f6d2f75706c6f6164732f656469746f722f65363165653733322d363665342d343936312d383362622d3334613038363534653335342f313534313036303338333634342e706e67)  

一对句子的分类任务：例如自然语言推断 (MNLI)，句子语义等价判断 (QQP) 等，如上图 (a) 所示，需要将两个句子传入 BERT，然后使用 [CLS] 的输出值 C进行句子对分类。  

单个句子分类任务：例如句子情感分析 (SST-2)，判断句子语法是否可以接受 (CoLA) 等，如上图 (b) 所示，只需要输入一个句子，无需使用 [SEP] 标志，然后也是用 [CLS] 的输出值 C 进行分类。  

问答任务：如 SQuAD v1.1 数据集，样本是语句对 (Question, Paragraph)，Question 表示问题，Paragraph 是一段来自 Wikipedia 的文本，Paragraph 包含了问题的答案。而训练的目标是在 Paragraph 找出答案的起始位置 (Start，End)。如上图 (c) 所示，将 Question 和 Paragraph 传入 BERT，然后 BERT 根据 Paragraph 所有单词的输出预测 Start 和 End 的位置。  

单个句子标注任务：例如命名实体识别 (NER)，输入单个句子，然后根据 BERT 对于每个单词的输出 T预测这个单词的类别，是属于 Person，Organization，Location，Miscellaneous 还是 Other (非命名实体)。  

Word2Vec 的 CBOW：通过单词 i 的上文和下文信息预测单词 i，但是采用的是词袋模型，不知道单词的顺序信息。例如预测单词 "自然" 的时候，会同时采用上文 "我/喜欢/学习" 和下文 "语言/处理" 进行预测。CBOW 在训练时是相当于把 "自然" 这个单词 Mask 的。  

ELMo：ELMo 在训练的时候使用 biLSTM，预测 "自然" 的时候，前向 LSTM 会 Mask "自然" 之后的所有单词，使用上文 "我/喜欢/学习" 预测；后向 LSTM 会 Mask "自然" 之前的单词，使用下文 "语言/处理" 进行预测。然后再将前向 LSTM 和后向 LSTM 的输出拼接在一起，因此 ELMo 是将上下文信息分隔开进行预测的，而不是同时利用上下文信息进行预测。  

OpenAI GPT：OpenAI GPT 是另外一种使用 Transformer 训练语言模型的算法，但是 OpenAI GPT 使用的是 Transformer 的 Decoder，是一种单向的结构。预测 "自然" 的时候只使用上文 "我/喜欢/学习"，Decoder 中包含了 Mask 操作，将当前预测词之后的单词都 Mask。  

BERT 的作者认为在预测单词时，要同时利用单词 left (上文) 和 right (下文) 信息才能最好地预测。将 ELMo 这种分别进行 left-to-right 和 right-to-left 的模型称为 shallow bidirectional model (浅层双向模型)，BERT 希望在 Transformer Encoder 结构上训练出一种深度双向模型 deep bidirectional model，因此提出了 Mask LM 这种方法进行训练。  

Mask LM 是用于防止信息泄露的，例如预测单词 "自然" 的时候，如果不把输入部分的 "自然" Mask 掉，则预测输出的地方是可以直接获得 "自然" 的信息。  

BERT 在训练时只预测 [Mask] 位置的单词，这样就可以同时利用上下文信息。但是在后续使用的时候，句子中并不会出现 [Mask] 的单词，这样会影响模型的性能。因此在训练时采用如下策略，随机选择句子中 15% 的单词进行 Mask，在选择为 Mask 的单词中，有 80% 真的使用 [Mask] 进行替换，10% 不进行替换，剩下 10% 使用一个随机单词替换。  

BERT 的第二个预训练任务是 Next Sentence Prediction (NSP)，即下一句预测，给定两个句子 A 和 B，要预测句子 B 是否是句子 A 的下一个句子。  

BERT 使用这一预训练任务的主要原因是，很多下游任务，例如问答系统 (QA)，自然语言推断 (NLI) 都需要模型能够理解两个句子之间的关系，但是通过训练语言模型达不到这个目的。  

BERT 在进行训练的时候，有 50% 的概率会选择相连的两个句子 A B，有 50% 的概率会选择不相连得到两个句子 A B，然后通过 [CLS] 标志位的输出 C预测句子 A 的下一句是不是句子 B。  

输入 = [CLS] 我 喜欢 玩 [Mask] 联盟 [SEP] 我 最 擅长 的 [Mask] 是 亚索 [SEP]类别 = B 是 A 的下一句  
输入 = [CLS] 我 喜欢 玩 [Mask] 联盟 [SEP] 今天 天气 很 [Mask] [SEP]类别 = B 不是 A 的下一句  

因为 BERT 预训练时候采用了 Masked LM，每个 batch 只会训练 15% 的单词，因此需要更多的预训练步骤。ELMo 之类的顺序模型，会对每一个单词都进行预测。  

BERT 使用了 Transformer 的 Encoder 和 Masked LM 预训练方法，因此可以进行双向预测；而 OpenAI GPT 使用了 Transformer 的 Decoder 结构，利用了 Decoder 中的 Mask，只能顺序预测。  


### 十二、[什么是BERT？](https://zhuanlan.zhihu.com/p/98855346)  

BERT 的全称为 Bidirectional Encoder Representation from Transformers，是一个预训练的语言表征模型。它强调了不再像以往一样采用传统的单向语言模型或者把两个单向语言模型进行浅层拼接的方法进行预训练，而是采用新的 masked language model（MLM），以致能生成深度的双向语言表征。BERT 论文发表时提及在 11 个 NLP（Natural Language Processing，自然语言处理）任务中获得了新的 state-of-the-art 的结果，令人目瞪口呆。    

该模型有以下主要优点：  

1）采用 MLM 对双向的 Transformers 进行预训练，以生成深层的双向语言表征。  

2）预训练后，只需要添加一个额外的输出层进行 fine-tune，就可以在各种各样的下游任务中取得 state-of-the-art 的表现。在这过程中并不需要对 BERT 进行任务特定的结构修改。   

为了完成具体的分类任务，除了单词的 token 之外，作者还在输入的每一个序列开头都插入特定的分类 token（[CLS]），该分类 token 对应的最后一个 Transformer 层输出被用来起到聚集整个序列表征信息的作用。  

由于 BERT 是一个预训练模型，其必须要适应各种各样的自然语言任务，因此模型所输入的序列必须有能力包含一句话（文本情感分类，序列标注任务）或者两句话以上（文本摘要，自然语言推断，问答任务）。那么如何令模型有能力去分辨哪个范围是属于句子 A，哪个范围是属于句子 B 呢？BERT 采用了两种方法去解决：  

1）在序列 tokens 中把分割 token（[SEP]）插入到每个句子后，以分开不同的句子 tokens。  

2）为每一个 token 表征都添加一个可学习的分割 embedding 来指示其属于句子 A 还是句子 B。   

Transformer的特点就是有多少个输入就有多少个对应的输出（存疑，注意一下是不是这样以及为什么是这样）  

C 为分类 token（[CLS]）对应最后一个 Transformer 的输出，T 则代表其他 token 对应最后一个 Transformer 的输出。对于一些 token 级别的任务（如，序列标注和问答任务），就把 T 输入到额外的输出层中进行预测。对于一些句子级别的任务（如，自然语言推断和情感分类任务），就把 C 输入到额外的输出层中，这里也就解释了为什么要在每一个 token 序列前都要插入特定的分类 token。    

最后训练样例长这样：  

Input1=[CLS] the man went to [MASK] store [SEP] he bought a gallon [MASK] milk [SEP]  

Label1=IsNext  

Input2=[CLS] the man [MASK] to the store [SEP] penguin [MASK] are flight ##less birds [SEP]  

Label2=NotNext  

把每一个训练样例输入到 BERT 中可以相应获得两个任务对应的 loss，再把这两个 loss 加在一起就是整体的预训练 loss。（也就是两个任务同时进行训练）  

可以明显地看出，这两个任务所需的数据其实都可以从无标签的文本数据中构建（自监督性质），比 CV 中需要人工标注的 ImageNet 数据集可简单多了。    


### 十三、[彻底搞懂 BERT](https://www.cnblogs.com/rucwxb/p/10277217.html)  

传统意义上来讲，词向量模型是一个工具，可以把真实世界抽象存在的文字转换成可以进行数学公式操作的向量，而对这些向量的操作，才是 NLP 真正要做的任务。因而某种意义上，NLP 任务分成两部分，预训练产生词向量，对词向量操作（下游具体 NLP 任务）。    





### Wikipedia  

上下文无关模型（如 word2vec 或 GloVe）为词汇表中的每个单词生成一个词向量表示，因此容易出现单词的歧义问题。BERT 考虑到单词出现时的上下文。例如，词“水分”的 word2vec 词向量在“植物需要吸收水分”和“财务报表里有水分”是相同的，但 BERT 根据上下文的不同提供不同的词向量，词向量与句子表达的句意有关。   




