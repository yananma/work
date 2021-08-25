
### 这里是写和 Python 相关的稍微长一些的代码  


#### 08.24 整理标注数据，返回格式是四个标签和标签对应的单词  

改进版本  

```python 
import json

import pandas as pd


def read_label(label_file_name):
    """
    读取标签文件，获得每一条标签的 id 和 id 所对应的词
    :param label_file_name: 文件名
    :return: 标签列表
    """
    li = []
    with open(label_file_name, encoding="utf-8") as fl:
        label_lines = json.load(fl)
        for label_line in label_lines:
            li.append(label_line)
    return li


def map_label(li):
    """
    完成标签 id 和词的映射
    :param li: 传入标签列表
    :return: 返回映射字典
    """
    d = {}
    for item in li:
        d[item['id']] = item['text']
    return d


label_list = read_label('label_config.json')
map_labels = map_label(label_list)

# print(map_labels)  # {105: '是', 106: '标志', 108: '犹豫', 109: '主体'}

final_list = []
with open('yuce_EN_840.jsonl', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        final_dict = {}
        line = json.loads(line)
        final_dict['text'] = line['text']
        annotations = line['annotations']
        tmp_dict = {}  # 这个是各自的标签对应的句子里标注的词
        for annotation in annotations:
            start = int(annotation['start_offset'])
            end = int(annotation["end_offset"])
            word = line['text'][start:end]
            tmp_dict[map_labels[annotation['label']]] = word
        for label in tmp_dict.keys():
            final_dict[label] = tmp_dict[label]
        final_list.append(final_dict)

df = pd.DataFrame(final_list)
df.to_excel('标注.xlsx', index=False)
```


原版  

```python
import json

import pandas as pd


def read_label(label_file_name):
    """
    读取标签文件，获得每一条标签的 id 和 id 所对应的词
    :param label_file_name: 文件名
    :return: 标签列表
    """
    li = []
    with open(label_file_name, encoding="utf-8") as fl:
        label_lines = json.load(fl)
        for label_line in label_lines:
            li.append(label_line)
    return li


def map_label(li):
    """
    完成标签 id 和词的映射
    :param li: 传入标签列表
    :return: 返回映射字典
    """
    d = {}
    for item in li:
        d[item['id']] = item['text']
    return d


label_list = read_label('label_config.json')
map_labels = map_label(label_list)

print(map_labels)  # {105: '是', 106: '标志', 108: '犹豫', 109: '主体'}

final_list = []
with open('yuce_EN_840.jsonl', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        final_dict = {}
        line = json.loads(line)
        final_dict['text'] = line['text']
        annotations = line['annotations']
        final_dict["labels"] = []    # 这个是标签的名字，是标注的标签的名字，可能是一个，可能是两个等等
        tmp_dict = {}    # 这个是各自的标签对应的句子里标注的词
        for annotation in annotations:
            final_dict["labels"].append(map_labels[annotation['label']])  # annotation['label'] 是数字，map_labels 是值
            start = int(annotation['start_offset'])
            end = int(annotation["end_offset"])
            word = line['text'][start:end]
            tmp_dict[map_labels[annotation['label']]] = word
        final_dict_labels = final_dict.pop("labels")
        if final_dict_labels:
            for label in final_dict_labels:
                final_dict[label] = tmp_dict[label] 
        final_list.append(final_dict)


# df = pd.DataFrame(final_list)
# df.to_excel('标注.xlsx', index=False)
```


#### 08.18 整理标注数据  

(有一个问题就是不要一直写入文件读取文件，赋值给一个变量就好了)  

1、多个文件合并成一个文件  

```python 
new_file_name = 'yuce.jsonl'
file_names = ['yuce_1.jsonl', 'yuce_2.jsonl', 'yuce_3.jsonl', 'yuce_4.jsonl']
with open(new_file_name, 'a', encoding="utf-8") as fp:    # 这么写要特别要注意的一点是，起的别名不能一样  
    for file_name in file_names:
        with open(file_name, encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                    fp.write(line)
```

2、按文章内容 text 去重  

```python
import html

char_translate = str.maketrans({i: '' for i in
                                r"""!"#$%｜丨&'()*《》+＋,-—./:;<=>?@[\]^_`{|}~“．”？，！～＠＃％＾＊【】（）、。：；’／＼＿－＝
                                ☆★○●◎◇◆□€■△▲※→←↑↓¤♂♀〖〗『』」「‖〃‘……￥·"""})


def replace_all_not_word_char_to_null(s):
    return ''.join(s.casefold().translate(char_translate).split())


with open('yuce_result.jsonl', 'a', encoding="utf-8") as fp:
    with open("yuce.jsonl", encoding="utf-8") as f:
        count = 0
        lines = f.readlines()
        quchong_result = set()
        for line in lines:
            line = html.unescape(json.loads(line.strip()))
            text = line['text']
            clean_text = replace_all_not_word_char_to_null(text)
            if clean_text not in quchong_result:
                quchong_result.add(clean_text)
            else:
                continue
            fp.write(json.dumps(line) + '\n')
            count += 1
        print(count)
```

排序

指定排序规则的例子  

```python 
s = [
    ('he',2,9),
    ('t',1,8),
    ('m',2,3),
    ('k',1,9),
    ('j',1,2),
]

print(sorted(s,key=lambda x:(x[1],x[2])))

打印结果是：[('j', 1, 2), ('t', 1, 8), ('k', 1, 9), ('m', 2, 3), ('he', 2, 9)]  
```

添加标签数字列表(这种方法是可以的实现效果的，但是比较繁琐，因为要加一个字段，排完序以后还要再去掉这个字段，所以最后没有使用这种方法)  

```python
words = ["新兴", "突破", "颠覆", "前沿", "前景", "关键技术", "核心技术", "共性技术", "瓶颈", "难点",
         "困境", "难题", "短板", "卡脖子", "管制", "使能技术"]

with open('yuce_result1.jsonl', 'a', encoding="utf-8") as fp:
    with open('yuce_result.jsonl', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = json.loads(line.strip())
            text = line['text']
            li = []
            for i, word in enumerate(words):
                if word not in text:
                    li.append(0)
                else:
                    li.append(1)
            line['num'] = li
            fp.write(json.dumps(line) + '\n')

with open('yuce_result1.jsonl', encoding="utf-8") as f:
    lines = f.readlines()
    print(sorted(lines, key=lambda x: tuple((json.loads(x)["num"][i] for i in range(len(json.loads(x)["num"])))), reverse=True))
```

最后使用的方法  

```python 
words = ["新兴", "突破", "颠覆", "前沿", "前景", "关键技术", "核心技术", "共性技术", "瓶颈", "难点",
         "困境", "难题", "短板", "卡脖子", "管制", "使能技术"]

sorted_list = sorted(
    (json.loads(row) for row in open('yuce_result.jsonl', 'r', encoding='utf8')),
    key=lambda x: tuple(keyword in x['text'] for keyword in words),
    reverse=True
)

with open('final_sort_result.jsonl', 'a', encoding="utf-8") as f:
    for it in sorted_list:
        f.write(json.dumps(it) + '\n')
```

转成指定输出的格式，指定的格式为只包含 text 和 labels 两个键，text 的值就是 text，labels 的值是标签开始位置、标签结束位置和对应的标签组成的列表。  

```python 
import json

label_files = ['label_1.json', 'label_2.json', 'label_3.json', 'label_4.json']

li = []
for label_file in label_files:
    with open(label_file, 'r', encoding="utf-8") as fl:
        label_lines = json.load(fl)
        for label_line in label_lines:
            li.append(label_line)

d = {}
for item in li:
    d[item['id']] = item['text']

final_dict = {}
with open('result.json', 'a', encoding="utf-8") as fl:
    with open("final_sort_result.jsonl", 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = json.loads(line)
            final_dict["text"] = line['text']
            annotations = line['annotations']
            final_dict["labels"] = []
            for annotation in annotations:
                final_dict["labels"].append(
                    [annotation['start_offset'], annotation["end_offset"], d[annotation['label']]])
            print(final_dict)
            fl.write(json.dumps(final_dict) + "\n")
```



#### 08.16  

自己写的简单解决方法。  

```python 
li = [
    {
        'a': 6,
        'b': [
            {
                'c': True,
                'd': {
                    'e': [
                        {'k': 8, 'e': "xxx"},
                        {'k': 10, 'e': 'asdas'}
                    ],
                    'm': "asdasd"
                },
            },
            {
                'c': True,
                'd': {
                    'e': [
                        {'k': 123, 'e': "xxx"},
                        {'k': 120, 'e': 'asdas'}
                    ],
                    'm': "mmasdasssd"
                }
            }
        ]
    },
]


class Solution:

    def replace_to_default(self, list_of_items):
        for item in list_of_items:
            for key in item.keys():
                if type(item[key]) == list:
                    self.replace_to_default(item[key])
                elif type(item[key]) == dict:
                    self.replace_to_default([item[key]])
                else: 
                    item[key] = type(item[key])()
                # if isinstance(item[key], bool):
                #     item[key] = bool()
                # elif isinstance(item[key], str):
                #     item[key] = str()
                # elif isinstance(item[key], int):
                #     item[key] = int()
        return list_of_items


s = Solution()
print(s.replace_to_default(li))
```

彦彬的方法  

思想就是没有到底就继续拆，到底了就取默认值，有更强的容错性。  

```python 
class TransSimpleJson:

    @classmethod
    def visitor(cls, obj):
        if isinstance(obj, list):
            return cls.visitor_list(obj)
        elif isinstance(obj, dict):
            return cls.visitor_dict(obj)
        else:
            return cls.visitor_else(obj)

    @classmethod
    def visitor_list(cls, obj: list):
        return [cls.visitor(it) for it in obj]

    @classmethod
    def visitor_dict(cls, obj: dict):
        return {k: cls.visitor(v) for k, v in obj.items()}

    @classmethod
    def visitor_else(cls, obj):
        # 取默认值
        return obj.__class__()
        # # 取原本的值
        # return obj
        
print(TransSimpleJson().visitor(li))
```


#### 08.04  

```python 
import yaml
import re
from django.conf import settings
from django.core.management import BaseCommand

from data_analysis.connect import ESConnect, ConnectManager
from data_analysis.piplines.es_craw_module import ESSpider

from pathlib import Path


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-file',
            dest='file',
            default=settings.RESOURCE_ROOT / 'docs' / 'program' / 'ZKY_MAP_SETTING.yaml',
            help='配置的yaml文件',
        )
        parser.add_argument(
            '-si',
            dest='sindex',
            default='test-zky',
            help='查询的索引',
        )

    def handle(self, *args, **options):
        client: ESConnect = ConnectManager.ES.get_setting('DEBUG')
        source_yaml = yaml.load(Path(options['file']).open('r', encoding='utf-8'), Loader=yaml.FullLoader)
        source_data = source_yaml.get('zky_exclude_words', None)

        query_dict = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [

                                ]
                            }
                        },
                        {
                            "range": {
                                "post_time": {
                                    "gte": "2021-05-04 00:00:00",
                                    "lt": "2021-08-05 00:00:00"
                                }
                            }
                        }
                    ]
                }
            },
        }
        for data in source_data:
            query_dict["query"]["bool"]['must'][0]['bool']['should'].extend([
                {
                    "match":{
                        "title":data
                    }
                },
                {
                    "match":{
                        'text':data
                    }
                }
            ])


        for data, next_search_after in ConnectManager.ES.get_setting('DEFAULT').search_by_page_with_searchafter(
                options['sindex'],
                doc=None,
                fields=['title', 'text'],
                query=query_dict,
                sort_fields=[{'post_time': 'desc'}, {'include_time': 'desc'}],
                return_sort=True
        ):
            titles = [it['title'] for it in data]
            break


        with (settings.RESOURCE_ROOT / 'docs' / 'program' / 'result.txt').open('w',encoding='utf8') as fp:
            for title in titles:
                title = re.sub(r'(<.*?>)|(\n)', '', title)    # 去掉标签和换行
                fp.write(title + '\n')
```

改成  

```python 
import yaml
import re
from django.conf import settings
from django.core.management import BaseCommand

from data_analysis.connect import ESConnect, ConnectManager
from data_analysis.piplines.es_craw_module import ESSpider

from pathlib import Path


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-file',
            dest='file',
            default=settings.RESOURCE_ROOT / 'docs' / 'program' / 'ZKY_MAP_SETTING.yaml',
            help='配置的yaml文件',
        )
        parser.add_argument(
            '-si',
            dest='sindex',
            default='test-zky',
            help='查询的索引',
        )

    def handle(self, *args, **options):
        client: ESConnect = ConnectManager.ES.get_setting('DEBUG')
        source_yaml = yaml.load(Path(options['file']).open('r', encoding='utf-8'), Loader=yaml.FullLoader)
        source_data = source_yaml.get('zky_exclude_words', None)

        query_dict = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "bool": {
                                        "should": [
                                            {
                                                "query_string": {
                                                    "fields": ['title', 'text'],
                                                    "query":' OR '.join(f'"{it}"' for it in source_data)
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "range": {
                                        "post_time": {
                                            "gte": "2021-05-04 00:00:00",
                                            "lt": "2021-08-05 00:00:00"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                }


        for data, next_search_after in ConnectManager.ES.get_setting('DEFAULT').search_by_page_with_searchafter(
                options['sindex'],
                doc=None,
                fields=['title', 'text'],
                query=query_dict,
                sort_fields=[{'post_time': 'desc'}, {'include_time': 'desc'}],
                return_sort=True
        ):
            titles = [it['title'] for it in data]
            break


        with (settings.RESOURCE_ROOT / 'docs' / 'program' / 'result.txt').open('w',encoding='utf8') as fp:
            for title in titles:
                title = re.sub(r'(<.*?>)|(\n)', '', title)    # 去掉标签和换行
                fp.write(title + '\n')

```


#### 07.29  

```python 
class MyRequest:
    def __init__(self, query_param, data_param):
        self.query_param = query_param
        self.data_param = data_param


request1 = MyRequest(
    query_param={
        'ts': '114514',
        'name': 'syb'
    },
    data_param={
        'password': '1234567'
    }
)


import functools


def arg_wrap(arg_name, must_in_place=None, arg_type=None, arg_validate=None):
    def outer(func):
        @functools.wraps(func)
        def inner(request,*args, **kwargs):
            if must_in_place is None:
                arg_value = request.query_param.get(arg_name, None) or request.data_param.get(arg_name, None)
            elif must_in_place in ['query_param','data_param']:
                arg_value = getattr(request,must_in_place,None)
            # elif must_in_place == 'query_param':
            #     arg_value = request.query_param.get(arg_name, None)
            # elif must_in_place == 'data_param':
            #     arg_value = request.data_param.get(arg_name, None)

            if arg_type is not None:
                arg_value = arg_type(arg_value)

            if arg_validate is not None:
                result = arg_validate(arg_value)
                if result is False:
                    raise Exception

            if getattr(request, 'ARGS', None) is None:
                request.ARGS = {arg_name: arg_value}
            else:
                request.ARGS[arg_name]= arg_value

            # print(getattr(request, 'query_param'))
            res = func(request, *args, **kwargs)
            return res
        return inner
    return outer


@arg_wrap('name', must_in_place='query_param')
@arg_wrap('ts', arg_type=int)
@arg_wrap('password', arg_validate=lambda x:len(x)>6)
def my_func(request):
    print('success in view func')
    print(request.query_param)
    print(request.data_param)
    print(request.ARGS)
    print('***********')


my_func(request1)
```


#### 07.28  

```python
# add_tag函数会替换成 "\t这是一个字符串，有<TAG country='中国'>中科院</TAG>这个单词   "
# normalize会去除上一步空格、标点符号等变成 "这是一个字符串TAGcountry中国中科院TAG这个单词"
# s = TextTools('\t这是一个字符串，有中科院这个单词   ').add_tag(source='中科院' ,target='中国').normalize()
# print(s) # 打印 "这是一个字符串TAGcountry中国中科院TAG这个单词"

from collections import UserString
import re


class TextTools(UserString):

    def __init__(self, s):
        self.data = s

    def add_tag(self, source, target):
        self.data = re.sub(source, "<TAG country='{}'>{}</TAG>".format(target, source), self.data)
        return self

    def normalize(self):
        self.data = re.sub(r'[<>=\'\'/ ，]', '', self.data).strip()
        return self


print(TextTools('\t这是一个字符串，有中科院这个单词   ').add_tag(source='中科院', target='中国').normalize())
```


改进方法  

```python         
def add_tag(self, source, target):
    self.data = re.sub(f'({source})', r"<TAG country='{}'>\1</TAG>".format(target), self.data)
    return self

# f'({source})' 和下面的内容是等价的  
# s = '({})'.format(source)
```


