



#### 08.18 

多个文件合并成一个文件（写的不好，有待优化）

```python 
new_file_name = 'yuce.jsonl'
file_names = ['yuce_1.jsonl', 'yuce_2.jsonl', 'yuce_3.jsonl', 'yuce_4.jsonl']
for file_name in file_names:
    with open(file_name, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            with open(new_file_name, 'a', encoding="utf-8") as fp:
                fp.write(line)
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
