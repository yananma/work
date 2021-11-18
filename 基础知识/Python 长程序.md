
### 这里是写和 Python 相关的稍微长一些的代码  


#### LAC 分词 11.17 

```python 
import logging
import time

from LAC import LAC
from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd

logger = logging.getLogger('mxlog')


class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout=None, stderr=None, no_color=False, force_color=False)
        self.lac = LAC(mode='lac')

    def add_arguments(self, parser):
        self.lac.load_customization(str(settings.RESOURCE_ROOT / 'docs' / 'program' / 'lac_person_costom.txt'))

    def handle(self, *args, **options):
        result_list = []
        df = pd.read_csv(str(settings.RESOURCE_ROOT / 'docs' / 'program' / 'pika.csv'))
        print(len(df))
        start = time.time()
        for line in df.iterrows():
            result_dict = {}
            text = line[1]['text'].strip()
            if not text:
                continue
            tag_text = ''.join(f'<{t}>{w}</{t}>' for w, t in zip(*self.lac.run(text)))
            result_dict['title'] = line[1]['title'] 
            result_dict['text'] = line[1]['text'] 
            result_dict['url'] = line[1]['url'] 
            result_dict['post_time'] = line[1]['post_time']
            result_list.append(result_dict)

        print('用时 %.2f sec' % (time.time() - start))

        data_frame = pd.DataFrame(result_list)
        data_frame.to_csv(str(settings.RESOURCE_ROOT / 'docs' / 'program' / 'pika_tag.csv'), index=False, sep=',')
        print('写入完毕。。。。。。')
```


#### 从 es 取数据，过动词匹配，title 去重 11.17   

```python 
import re

import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand

from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-si',
            dest='sindex',
            default='page',
            help='查询的索引',
        )

    def handle(self, *args, **options):
        source_data = ["说，", "说。", "说：", "说道，", "说道。", "表示，", "表示。", "回答：", "回答道", "呼吁，", "呼吁：", "强调，", "介绍，", "介绍道，",
                       "认为", "坦言，", "指出：", "看来，", "称，", "称。", "建议，", "建议。", "建议：", "她建议", "他建议", "建议包括", "提到，", "提到：",
                       "提出，", "告诉记者", "指出，", "报道，", ]
        verb_pat = re.compile("(" + ")|(".join(source_data) + ")")

        query_dict = {
            "query": {
                "bool": {
                    "filter": {
                        "bool": {
                            "must": [
                                {
                                    "range": {
                                        "post_time": {
                                            "gte": "2021-01-01 00:00:00",
                                            "lt": "2022-01-01 00:00:00"
                                        }
                                    }
                                },
                                {
                                    "match_phrase": {
                                        "text": "皮卡"
                                    }
                                },
                                {
                                    "term": {
                                        "site_name": {
                                            "value": "媒体库"
                                        }
                                    }
                                },
                                {
                                    "query_string": {
                                        "fields": ["text"],
                                        "query": ' OR '.join(f'"{data}"' for data in source_data)
                                    }
                                },
                                {
                                    "bool": {
                                        "must_not": [
                                            {
                                                "match_phrase": {
                                                    "text": "皮卡丘"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

        result_list = []
        for batch_data in ConnectManager.ES.get_setting('DEFAULT').search_by_page_with_searchafter(
                options['sindex'],
                doc=None,
                fields=["text", 'title', 'url', 'post_time'],
                query=query_dict,
                sort_fields=[{'post_time': 'desc'}, {'include_time': 'desc'}],
                return_sort=False,
                size=10000
        ):
            for data in batch_data:
                text = data['text']
                m = verb_pat.search(text)
                if m:
                    result_list.append(data)
                    continue
                else:
                    if re.search(r'据([^称,\.，。？\?!！;；]+?)称|据([^称,\.，。？\?!！;；]+?)报道', text):
                        result_list.append(data)
                        continue
            print('next batch')

        print(len(result_list))

        true_data_list = []
        title_dedupe_set = set()
        for data in result_list:
            title = TextFactory(data['title']).replace_all_not_word_char_to_null().now
            if title not in title_dedupe_set:
                title_dedupe_set.add(title)
                true_data_list.append(data)
            else:
                continue

        data_frame = pd.DataFrame(true_data_list)
        data_frame.to_csv(str(settings.RESOURCE_ROOT / 'docs' / 'program' / 'pika.csv'), index=False, sep=',')
```


#### 找所有 keyword 的位置 11.16 

```python 
def find_keyword_idx(keyword, text):
    keyword_idx = []
    if len(keyword) > 0:
        pos = text.find(keyword)
        while pos >= 0:
            keyword_idx.append([pos, pos + len(keyword)])
            pos = text.find(keyword, pos+1)
    return keyword_idx 
```


#### 读两个 JSON 文件，写入到一个 JSON 文件中 11.10

```python 
with open(origin_json_file, encoding='utf-8') as of:
    with open(predict_json, encoding='utf-8') as pf:
        with open('concate_dev.json', 'a', encoding='utf-8') as cf:
            for o_line, p_line in zip(of, pf):
                o_line, p_line = json.loads(o_line), json.loads(p_line) 
                o_line['predict_label'] = p_line['label'] 
                cf.write(json.dumps(o_line) + '\n')
                
with open('concate_dev_unicode.json', encoding='utf-8') as f:
    with open('error_examples.json', 'a', encoding='utf-8') as fp:
        for line in f:
            line = json.loads(line)
            if line['label'] != int(line['predict_label']):
                fp.write(json.dumps(line) + '\n')
            else:
                continue
```


#### 更新治理 flag 字段脚本 11.09  

```python 
import bisect
import logging
import argparse
import re
from itertools import islice
import csv
import json

from common.es_opts import get_point_datas, bulk_point_datas, BulkModeEnum
from common.filters.base import BaseKeyFilter
from common.models import ZKYDataVersion
from common.mx_simhash import compute_simhash_v2
from common.text_tools import TextFactory
from common.utils import today, SectionCheck, trans_to_md5, AuthorNameSearchTool, lastday
from resources.YUCE_KEYWORDS import NORMAL_KEYWORDS
from yuce.yuce_process import Yuce
from enum import Enum
from typing import Union, Tuple, List, Dict

from elasticsearch import helpers

from common.ESConnect import es_default_connect
from common.text_tools import TextFactory
from common.utils import today, trans_to_md5

logger = logging.getLogger(__file__)

logger.setLevel(logging.INFO)
logger_handle = logging.StreamHandler()
formater = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
logger_handle.setFormatter(formater)
logger.addHandler(logger_handle)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--version", default=__file__, type=str,
                        help="数据处理版本，用于区别各个不同的进程")
    parser.add_argument("--last", default=-1, type=int,
                        help="ES获取专家观点数据时间的几天前开始跑")
    parser.add_argument("--from_date", default='2020-01-01 00:00:00', type=str,
                        help="ES获取专家观点数据的起始时间")
    parser.add_argument("--to_date", default=today(time_str=None,to_datetime_str=True), type=str,
                        help="ES获取专家观点数据的结束时间")

    parser.add_argument("--rank", default=-1, type=int,
                        help="处理进程ID，默认主进程为-1")
    parser.add_argument("--bulk_count", default=100, type=int,
                        help="满多少bulk一次")
    parser.add_argument("--point_index", default='zhuanjiav2', type=str,
                        help="专家观点所在索引")
    parser.add_argument("--zhili_index", default='zhili-zky', type=str,
                        help="治理文本的索引")
    parser.add_argument("--search_time_field", default='post_time', type=str,
                        help="ES搜索时，from_date生效的时间字段")
    parser.add_argument("--time_desc", action='store_true',
                        help="时间是否倒序")

    args = parser.parse_args()

    if args.last>=0:
        args.from_date = lastday(args.last,time_str='00:00:00',to_datetime_str=True)
    logger.info('初始化VersionData')
    # 初始化date_version
    version_obj,created = ZKYDataVersion.get_or_create(
        version=f'{args.version}_{args.from_date.split()[0]}_{args.to_date.split()[0]}',
        defaults={
            'state':1
        }
    )
    search_after = json.loads(version_obj.search_after)

    all_count = 0
    logger.info(f'will read es datas,search_after is {search_after}')

    zhili_origin_bulk_results = []
    zhili_bulk_results = []
    for datas,next_search_after in get_point_datas(index=args.point_index,
                                                   doc="zhili_doc",
                                                   search_after=search_after,
                                                   fields=['flag','flag_range', 'zhili_text'],
                                                   from_date=args.from_date,
                                                   to_date=args.to_date,
                                                   sort_fields=[{args.search_time_field:'desc' if args.time_desc else 'asc'}],
                                                   search_time_field=args.search_time_field):
        logger.info(f'read es datas finish,count:{len(datas)}')
        zhili_bulk_results = []
        for data in datas:
            zhili_data_dict = {"zhili_text": data['zhili_text']}
            flag_split_list = data['flag'].split('#')
            for flag_index, flag in enumerate(flag_split_list):
                if flag == "科研基础设施":
                    flag_split_list[flag_index] = "科研基础设施建设"
                    zhili_data_dict['flag'] = '#'.join(flag_split_list)
                    data_flag_range = json.loads(data['flag_range'])
                    logger.info(data_flag_range)
                    for tag_index, (*_, ((_, keyword),)) in enumerate(data_flag_range):
                        if keyword == "科研基础设施":
                            data_flag_range[tag_index][3][0][1] = "科研基础设施建设"
                            zhili_data_dict['flag_range'] = json.dumps(data_flag_range)
                    zhili_bulk_results.append(zhili_data_dict)
                else:
                    continue
            if len(zhili_bulk_results):
                logger.info(f'will bulk zhili data,count:{len(zhili_bulk_results)}')
                success,faild = bulk_point_datas(
                    zhili_bulk_results,
                    index=args.zhili_index,
                    doc='zhili_doc',
                    op_type = BulkModeEnum.IF_EXISTS_UPDATE,
                    id_func=lambda post:trans_to_md5(TextFactory(post['zhili_text']).replace_all_not_word_char_to_null().now)
                )
                logger.info(f'bulk zhili data success:{success} faild:{faild}')
                # 更新 dataversion
                zhili_bulk_results.clear()
        version_obj.search_after = json.dumps(next_search_after)
        version_obj.save()
    logger.info('完成')
```


#### 10.14 修改 yuce 索引一个字段脚本  

```python 
import bisect
import logging
import argparse
import re
from itertools import islice
import csv
import json

from common.es_opts import get_point_datas, bulk_point_datas, BulkModeEnum
from common.filters.base import BaseKeyFilter
from common.models import ZKYDataVersion
from common.mx_simhash import compute_simhash_v2
from common.text_tools import TextFactory
from common.utils import today, SectionCheck, trans_to_md5, AuthorNameSearchTool, lastday
from resources.YUCE_KEYWORDS import NORMAL_KEYWORDS
from yuce.yuce_process import Yuce
from enum import Enum
from typing import Union, Tuple, List, Dict

from elasticsearch import helpers

from common.ESConnect import es_default_connect
from common.text_tools import TextFactory
from common.utils import today, trans_to_md5

logger = logging.getLogger(__file__)

logger.setLevel(logging.INFO)
logger_handle = logging.StreamHandler()
formater = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
logger_handle.setFormatter(formater)
logger.addHandler(logger_handle)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    ## Required parameters
    parser.add_argument("--version", default=__file__, type=str,
                        help="数据处理版本，用于区别各个不同的进程")
    parser.add_argument("--from_date", default='2020-01-01 00:00:00', type=str,
                        help="ES获取专家观点数据的起始时间")
    parser.add_argument("--last", default=-1, type=int,
                        help="ES获取专家观点数据时间的几天前开始跑")
    parser.add_argument("--to_date", default=today(time_str=None, to_datetime_str=True), type=str,
                        help="ES获取专家观点数据的结束时间")

    parser.add_argument("--rank", default=-1, type=int,
                        help="处理进程ID，默认主进程为-1")
    parser.add_argument("--chunk_count", default=100, type=int,
                        help="分批次处理数据的每批次的数量")
    parser.add_argument("--debug", action='store_true',
                        help="开启调试模式")
    parser.add_argument("--store_backup", action='store_true',
                        help="是否上数据到backup里")
    parser.add_argument("--point_index", default='zhuanjiav2', type=str,
                        help="专家观点所在索引")
    parser.add_argument("--yuce_index", default='yuce-zky', type=str,
                        help="预测文本的索引")
    parser.add_argument("--search_time_field", default='post_time', type=str,
                        help="ES搜索时，from_date生效的时间字段")
    parser.add_argument("--time_desc", action='store_true',
                        help="时间是否倒序")

    args = parser.parse_args()
    if args.last >= 0:
        args.from_date = lastday(args.last, time_str='00:00:00', to_datetime_str=True)

    logger.info('初始化VersionData')
    # 初始化date_version
    version_obj, created = ZKYDataVersion.get_or_create(
        version=args.version or f'{__file__}_{args.from_date.split()[0]}_{args.to_date.split()[0]}',
        defaults={
            'state': 1
        }
    )

    yuce = Yuce(args.rank)
    search_after = json.loads(version_obj.search_after)
    sentenceCheckTool = SectionCheck(BaseKeyFilter([[v[0], v[1:], [], []] for k, v in NORMAL_KEYWORDS.items()]), {})
    authorNameTool = AuthorNameSearchTool()
    logger.info(f'will read es datas,search_after is {search_after}')

    # stop_char = ["\?", "\!", "。", "？", "！"]
    # turn_char = ["\r", "\n"]

    stop_cpl = re.compile(r"[\?\!。？！]")
    stop_reverse_cpl = re.compile(r"(?:.*?[\?\!。？！])+")
    turn_cpl = re.compile(r"[\r\n]")
    turn_reverse_cpl = re.compile(r"(?:.*?[\r\n])+")

    def get_datas(index='zhuanjia', doc='zj_doc', from_date: str = '2020-01-01 00:00:00',
                  to_date: str = today(time_str=None, to_datetime_str=True), fields=None, search_after=None,
                  sort_fields=[{'post_time': 'desc'}], search_time_field='post_time') -> Tuple[List[Dict], List[str]]:
        es_conn = es_default_connect()
        query_dict = {
            'query': {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "default_field": search_time_field,
                                "query": f"[\"{from_date}\"  TO \"{to_date}\"]"
                            }
                        }
                    ]
                }
            },
            **(
                {'search_after': search_after} if search_after else {}
            )
        }
        for data in es_conn.search_by_page_with_searchafter(index, query=query_dict, fields=fields, return_sort=True,
                                                            doc=doc, sort_fields=sort_fields, size=2000):
            yield data

    for datas, next_search_after in get_datas(index=args.point_index, doc='yuce_doc', search_after=search_after,
                                              fields=['point_text', 'text', 'is_split', 'can_split',
                                                      'flag_range', 'post_time', 'yuce_author', 'yuce_text'], from_date=args.from_date,
                                              to_date=args.to_date):
        logger.info(f'read es datas finish,count:{len(datas)}')

        for data in datas:
            true_point_datas = set()
            for flag_range in data['flag_range']:
                flag_start_offset = flag_range[0]
                flag_end_offset = flag_range[1]
                if data['can_split'] and not data['is_split']:
                    forward_search = turn_reverse_cpl.search(data['text'], 0, flag_start_offset)
                    if forward_search:
                        start_offset = forward_search.end()
                    else:
                        start_offset = 0
                    afterward_search = turn_cpl.search(data['text'], flag_end_offset)
                    if afterward_search:
                        end_offset = afterward_search.start()
                    else:
                        end_offset = len(data['text'])
                    data['point_text'] = data['text'][start_offset:end_offset+1].strip()
                    true_point_datas.add(data['point_text'])
                elif not data['is_split']:
                    # try:
                    forward_search = stop_reverse_cpl.search(data['text'], 0, flag_start_offset)
                    if forward_search:
                        start_offset = forward_search.end()
                    else:
                        start_offset = 0
                    # except:
                    #     logger.exception('错了！')
                    #     logger.info(data)
                    #     raise Exception
                    afterward_search = stop_cpl.search(data['text'], flag_end_offset)
                    if afterward_search:
                        end_offset = afterward_search.start()
                    else:
                        end_offset = len(data['text'])
                    data['point_text'] = data['text'][start_offset:end_offset+1].strip()
                    true_point_datas.add(data['point_text'])
            data['point_text'] = "\n".join(true_point_datas)

        success, failed = bulk_point_datas(datas, index=args.yuce_index, op_type=BulkModeEnum.IF_EXISTS_UPDATE,
                                           id_func=lambda post: trans_to_md5(
                                               post['yuce_author'] + '||' + TextFactory(
                                                   post['yuce_text']).replace_all_not_word_char_to_null().now)
                                           )
        logger.info(f'Chunk bulk origin finish. success:{success} faild:{failed}')
```


#### 09.29 跑数据命令，从一个 es 索引中取数据到另一个索引中  

```python 
import datetime

from django.core.management import BaseCommand

from data_analysis.connect import ConnectManager
from data_analysis.piplines.es_bluk_module import ESBulk
from data_analysis.tools.data_pipline import DataPipline
from data_analysis.tools.utils import get_logger
from user.utils import trans_to_md5

logger = get_logger(__file__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            dest='index',
            default='kejisousou-points-formal',  # 后面要拼月份
            help='插入到的ES的索引',
        )
        parser.add_argument(
            '-si',
            dest='sindex',
            default='kejisousou-points-formal-*',
            help='查询的索引',
        )

    def load_datas(self, options):
        for datas in ConnectManager.ES.get_setting('DEFAULT').search_by_page_with_searchafter(
                options['sindex'],
                doc=None,
                return_sort=False,
                no_sort=True,
        ):
            for post in datas:
                yield post

    def add_zky_include_time(self, post):
        post['zky_include_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return post

    def handle(self, *args, **options):
        # 获取当前完成状态信息
        points_bulk_module = ESBulk(bulk_index=options['index'], bulk_doc='zj_doc',
                                    op_type=ESBulk.BulkModeEnum.IF_NOT_EXISTS_CREATE,
                                    id_func=lambda post: trans_to_md5(post['point_text'][:100]),
                                    has_search_after=False, split_date=True)

        point_cache_posts = []
        # 定义中文pipline
        pipline = (
            DataPipline()
                .regist_func_by_data(self.add_zky_include_time)  # 添加日期
        )
        cache_size = 500
        for post in pipline(self.load_datas(options)):
            # 添加缓存
            point_cache_posts.append(post)
            # 大于cache_size进行专家观点提取和上ES
            if len(point_cache_posts) > cache_size:
                logger.info(f'will to zky es')
                try:
                    success, failed, _ = list(points_bulk_module.run(point_cache_posts))[0]
                    logger.info(f'bulk to zky es success:{success} failed:{failed}')
                except Exception as e:
                    logger.exception('bulk to zky es error')

                point_cache_posts.clear()
```


#### 09.22 英文版 excel 转 jsonl，两个标签，有空值，有大小写不匹配  

```python 
import json
import re
import pandas as pd


def excel_to_jsonl(file_name, label_name):
    df = pd.read_excel(f'{file_name}.xlsx', engine='openpyxl')
    text_list = list(df['text'])
    label_list = list(df[label_name])
    shi_list = list(df['是'])
    with open(f'{file_name}.jsonl', 'a', encoding="utf-8") as f:
        for i, text in enumerate(text_list):
            final_dict = {'text': text}
            if str(shi_list[i]) != 'nan':
                shi_re_result = re.search(re.escape(shi_list[i].lower()), text.lower())
                final_dict['labels'] = [[shi_re_result.start(), shi_re_result.end(), '是']]
            else:
                final_dict['labels'] = []
            re_result = re.search(re.escape(label_list[i].lower()), text.lower())
            final_dict['labels'].append([re_result.start(), re_result.end(), label_name])
            print(final_dict)
            f.write(json.dumps(final_dict) + "\n")


excel_to_jsonl('技术预测EN新增', '标志')
```


#### 09.14 把上一个改成了函数  

```python 
import json
import re
import pandas as pd


def excel_to_jsonl(file_name, label_name):
    df = pd.read_excel(f'{file_name}.xlsx', engine='openpyxl')
    text_list = list(df['句子'])
    label_list = list(df[label_name])
    with open(f'{file_name}.jsonl', 'a', encoding="utf-8") as f:
        for i, text in enumerate(text_list):
            final_dict = {'text': text}
            re_result = re.search(re.escape(label_list[i]), text)
            final_dict['labels'] = [[re_result.start(), re_result.end(), label_name]]
            print(final_dict)
            f.write(json.dumps(final_dict) + "\n")


excel_to_jsonl('技术预测前50', '标志')
```

多标签加两句  
```python 
# shi_re_result = re.search(re.escape(shi_re_result), text)    # 多标签  
# final_dict['labels'].append([shi_re_result.start(), shi_re_result.end(), '是'])            
```


#### 09.13 把 excel 文件转换成 jsonl 格式  

```python 
import json
import re
import pandas as pd


df = pd.read_excel('技术预测-短板-不空.xlsx', engine='openpyxl', nrows=530)

juzi_list = list(df['句子'])
biaozhi_list = list(df['标志'])

pattern = '短板'

with open('技术预测-短板-不空.jsonl', 'a', encoding="utf-8") as f:
    for sentence in juzi_list:
        final_dict = {}
        re_result = re.search(pattern, sentence)
        final_dict['text'] = sentence
        final_dict['labels'] = [[re_result.start(), re_result.end(), '标志']]
        print(final_dict)
        f.write(json.dumps(final_dict) + "\n")
```


#### 09.10 跑一批姓名规则列表，找出不符合规则的句子  

```python 
import re
import LAC
from django.conf import settings
import os
from data_analysis.tools.text_tools import TextFactory

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZKY_Backend.settings_test')


class XMLTagMatchNode:

    def __init__(self, tag=None, tag_re=None, val=None, val_re=None, count='', empty=False):
        if empty:
            self.tag, self.val, self.re_str = '', '', ''
            self.count = 0
        self.tag = tag or tag_re or r'([^<]+?)'
        self.val = val or val_re or r'([^<]+?)'
        self.count = count
        self.re_str = rf'((<({self.tag})>{self.val}</({self.tag})>){self.count})'

    def __add__(self, other):
        if not other.re_str:
            return self
        self.re_str = rf'{self.re_str}{other.re_str}'
        return self

    def __or__(self, other):
        if not other.re_str:
            return self
        self.re_str = rf'{self.re_str}|{other.re_str}'
        return self

    def __and__(self, other):
        if not other.re_str:
            return self
        self.re_str = rf'{self.re_str}{other.re_str}'
        return self

    def __str__(self):
        return self.re_str

    def __invert__(self):
        self.re_str = rf'(((?!{self.re_str}).)*?)'
        return self

    def reverse(self):
        self.re_str = rf'((.*?{self.re_str})+)'
        return self

    def to_re(self):
        return re.compile(self.re_str)


N = XMLTagMatchNode

lac = LAC.LAC(mode='lac')
lac.load_customization(str(settings.RESOURCE_ROOT/'docs'/'program'/'lac_person_costom.txt'))

origin_list = ['国外专业拆解机构IFixit首席执行官凯尔·维恩斯（Kyle Wiens）表示，',
               '百度创始人、董事长兼CEO李彦宏给出了自己的答案。',
               '江西南昌大学中国科学院院士，南昌大学副校长首席代表王光绪博士指出，南昌大学带来了世界上效率最高的黄光LED和绿光LED，',
               '宁德市委常委、常务副市长缪绍炜表示，发展通航产业要做好规划和论证工作，']

pattern = (
                N(tag_re='(LOC)|(ORG)')
                + ~(
                    N(tag='w', val_re=r'[^、·]')
                    |
                    N('WHITE')
                )
                + N('n')
                + N('PER')
            ).to_re()

cpl = re.compile(pattern)

for line in origin_list:
    text_with_tag = TextFactory(line).add_tag_from_lac(lac).now    # lac 打标签，输出的是带标签的文本    
    r = cpl.search(text_with_tag)
    if r:    # 按照规则匹配成功  
        # print(r.group())
        pass
    else:    # 按照规则匹配失败  
        print(line)
        print(text_with_tag + '\n')
```


#### 09.09 从 es 查聚合结果  

这个应该非常简单才是，结果花了很长时间。一个是函数用 search，而不是 search_by_page_with_searchafter，熟悉 search 函数花了一些时间。  

一个是时间转换，strptime 和 strftime  

一个是键值对匹配，本来这个非常简单，结果套用了原来复杂的代码，搞得很麻烦，也花了一些时间。  

```python
import pandas as pd
from django.conf import settings
from datetime import datetime
from django.core.management import BaseCommand

from data_analysis.connect import ConnectManager


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-si',
            dest='sindex',
            default='kejisousou-en-test',
            help='查询的索引',
        )

    def handle(self, *args, **options):

        query_dict = {
            "size": 0,
            "aggs": {
                "time_aggs": {
                    "date_histogram": {
                        "field": "post_time",
                        "time_zone": "+08:00",
                        "interval": "month",
                        "format": "yyyy-MM"
                    },
                    "aggs": {
                        "category_aggs": {
                            "terms": {
                                "field": "category.keyword"
                            }
                        }
                    }
                }
            }
        }

        final_list = []
        data = ConnectManager.ES.get_setting('DEFAULT').search(options['sindex'], size=0, body=query_dict)
        for month_data in data['aggregations']['time_aggs']['buckets']:
            final_dict = {'月份': datetime.strptime(month_data['key_as_string'], '%Y-%m').strftime('%Y年%m月'),
                          '全部数据': month_data['doc_count']}
            for category in month_data['category_aggs']['buckets']:
                key = category['key']
                count = category['doc_count']
                final_dict[key] = count
            final_list.append(final_dict)
            print(final_dict)
        data_frame = pd.DataFrame(final_list)
        data_frame.to_csv(str(settings.RESOURCE_ROOT / 'docs' / 'program' / '英文版每月分类统计.csv'), index=False, sep=',')

        print("完成......")
```


#### 09.04 把数据写入到数据库里（国家规则）  

写在 ZKY_Backend 的 data_analysis\management\commands\test.py 中就行，没有需要配置的参数，就是用 manage.py 运行 test 命令  

因为 manage.py 默认用的是 settings_test，所以不传参数的时候使用的就是测试数据库。  

如果要更新正式数据库，就要配置参数 --settings=ZKY_Backend.settings

```python 
import logging

import pandas as pd
from data_analysis.models import ZKYCountry
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger('mxlog')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-file',
            dest='file',
            default=settings.RESOURCE_ROOT / 'docs' / 'program' / 'country_rule V4.xlsx',
            help='配置的yaml文件',
        )

    def handle(self, *args, **options):
        # ZKYCountry.objects.all().delete()
        df: pd.DataFrame = pd.read_excel(options['file'].__str__(), )
        field_list = ['synonyms', 'limiter', 'exclude_limiter', 'level']
        for d in df.iterrows():
            ZKYCountry.objects.update_or_create(
                name=d[1]["name"],
                defaults={field: d[1][field] if d[1][field] == d[1][field] else '' for field in field_list}  # 使用字典推导式

                # defaults={
                #     'synonyms': d[1]["synonyms"] if d[1]["synonyms"] == d[1]["synonyms"] else '',
                #     'limiter': d[1]["limiter"] if d[1]["limiter"] == d[1]["limiter"] else '',
                #     'exclude_limiter': d[1]["exclude_limiter"] if d[1]["exclude_limiter"] == d[1]["exclude_limiter"]
                #                        else '',
                #     'level': d[1]['level'] if d[1]["level"] == d[1]["level"] else '',
                # }
            )
        logger.info(f'完成')
```


#### 09.02 专家姓名规则匹配  

```python 
import re

import LAC
from django.core.management import BaseCommand

from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory


class XMLTagMatchNode:

    def __init__(self, tag=None, tag_re=None, val=None, val_re=None, count='', empty=False):
        if empty:
            self.tag, self.val, self.re_str = '', '', ''
            self.count = 0
        self.tag = tag or tag_re or r'([^<]+?)'
        self.val = val or val_re or r'([^<]+?)'
        self.count = count
        self.re_str = rf'((<({self.tag})>{self.val}</({self.tag})>){self.count})'

    def __add__(self, other):
        if not other.re_str:
            return self
        self.re_str = rf'{self.re_str}{other.re_str}'
        return self

    def __or__(self, other):
        if not other.re_str:
            return self
        self.re_str = rf'{self.re_str}|{other.re_str}'
        return self

    def __and__(self, other):
        if not other.re_str:
            return self
        self.re_str = rf'{self.re_str}{other.re_str}'
        return self

    def __str__(self):
        return self.re_str

    def __invert__(self):
        self.re_str = rf'(((?!{self.re_str}).)*?)'
        return self

    def reverse(self):
        self.re_str = rf'((.*?{self.re_str})+)'
        return self

    def to_re(self):
        return re.compile(self.re_str)


N = XMLTagMatchNode

lac = LAC.LAC(mode='lac')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-si',
            dest='sindex',
            default='kejisousou-points-test',
            help='查询的索引',
        )

    def handle(self, *args, **options):
        source_data = ["6G", "物联网", "人工智能", "5G", "无人驾驶"]

        query_dict = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "query_string": {
                                "fields": ["point_text"],
                                "query": ' OR '.join(f'"{data}"' for data in source_data)
                            }
                        }
                    ]
                }
            }
        }

        result_list = []
        for data, next_search_after in ConnectManager.ES.get_setting('DEFAULT').search_by_page_with_searchafter(
                options['sindex'],
                doc=None,
                fields=["point_text"],
                query=query_dict,
                sort_fields=[{'post_time': 'desc'}, {'include_time': 'desc'}],
                return_sort=True,
                limit=3000
        ):
            # print("开始查询......")
            result_text = [it['point_text'] for it in data]
            result_list.extend(result_text)
            print("查询结束......")
            break

        pattern = (N(tag_re='(LOC)|(ORG)') + ~N(tag='w', val_re=r'[^、·]') + N('n') + N('PER')).to_re()
        cpl = re.compile(pattern)
        per_cpl = re.compile(r"(<PER>.*?</PER>)+")

        chunk_text_list = []
        count = 0
        with open('not_match.txt', 'w', encoding='utf-8') as fs:
            for line in result_list:

                if line:
                    text_with_tag = TextFactory(line).add_tag_from_lac(lac).now
                    r = cpl.search(text_with_tag)
                    if r:
                        chunk_text_with_tag = TextFactory(text_with_tag).chunk_tag_with_max_size_v2(search_flag_str=r.group()).now.strip('…')
                        chunk_text_no_tag = TextFactory(chunk_text_with_tag).replace_tag_to_others().now
                        if chunk_text_no_tag not in chunk_text_list:
                            chunk_text_list.append(chunk_text_no_tag)
                            count += 1
                            fs.write(f'{TextFactory(r.group()).replace_tag_to_others().now}\n\t{chunk_text_no_tag}\n\n')
                            fs.write(f'{r.group()}\n\t{chunk_text_with_tag}\n\n')
                            fs.write('*' * 80 + '\n\n')
                            # print(f'{TextFactory(r.group()).replace_tag_to_others().now}\n\t{chunk_text_no_tag}\n')
                            # print(f'{r.group()}\n\t{chunk_text_with_tag}\n')
                            # print('*' * 80 + '\n')
                            if count % 100 == 0:
                                print(f'已经写入了{count}条数据。')
                            if count == 1000:
                                break
                        else:
                            continue
                    else:    # 如果按照规则没有匹配到，那么就搜 PER，如果存在 PER 就返回 PER 相关的一段；如果没有 PER 就 pass
                        per_r_list = per_cpl.findall(text_with_tag)
                        if per_r_list:
                            per_r_list = list(set(per_r_list))
                            for per_r in per_r_list:
                                chunk_text_with_tag = TextFactory(text_with_tag).chunk_tag_with_max_size_v2(
                                    search_flag_str=per_r).now.strip('…')
                                chunk_text_no_tag = TextFactory(chunk_text_with_tag).replace_tag_to_others().now
                                if chunk_text_no_tag not in chunk_text_list:
                                    chunk_text_list.append(chunk_text_no_tag)
                                    count += 1
                                    fs.write(f'{TextFactory(per_r).replace_tag_to_others().now}\n\t{chunk_text_no_tag}\n\n')
                                    fs.write(f'{per_r}\n\t{chunk_text_with_tag}\n\n')
                                    fs.write('*' * 80 + '\n\n')
                                    if count % 100 == 0:
                                        print(f'已经写入了{count}条数据。')
                                    if count == 1000:
                                        break
                                    # print(f'{TextFactory(per_r).replace_tag_to_others().now}\n\t{chunk_text_no_tag}\n')
                                    # print(f'{per_r}\n\t{chunk_text_with_tag}\n')
                                    # print('*' * 80 + '\n')
                                else:
                                    continue
                        else:
                            pass
```


#### 09.01 专家姓名规则  

写在 test.py 中就行，如果只有几条，就写到一个列表里。  

```python 
import logging

from LAC import LAC
from django.conf import settings
from django.core.management.base import BaseCommand
import pandas as pd


class Command(BaseCommand):
    def add_arguments(self, parser):
        self.lac = LAC(mode='lac')
        self.lac.load_customization(str(settings.RESOURCE_ROOT / 'docs' / 'program' / 'lac_person_costom.txt'))
        pass

    def handle(self, *args, **options):
        pmap = {
            'n': '普通名词',
            'f': '方位名词',
            's': '处所名词',
            'nw': '作品名',
            'nz': '其他专名',
            'v': '普通动词',
            'vd': '动副词',
            'vn': '名动词',
            'a': '形容词',
            'ad': '副形词',
            'an': '名形词',
            'd': '副词',
            'm': '数量词',
            'q': '量词',
            'r': '代词',
            'p': '介词',
            'c': '连词',
            'u': '助词',
            'xc': '其他虚词',
            'w': '标点符号',
            'PER': '人名',
            'LOC': '地名',
            'ORG': '机构名',
            'TIME': '时间',
        }
        li = []
        for line in (settings.RESOURCE_ROOT / 'docs' / 'program' / '姓名测试新的例子.txt').read_text(encoding='utf8').splitlines():
            line = line.strip()
            if not line:
                continue
            ws, ps = self.lac.run(line)
            li.append(ws)
            li.append(ps)
            li.append([pmap[p] for p in ps])
            li.append('\n')

        dataframe = pd.DataFrame(li)
        dataframe.to_csv(str(settings.RESOURCE_ROOT / 'docs' / 'program' / 'test_name.csv'), index=False, sep=',')
        print('写入完毕。。。。。。')
```


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

09.01 改成了 10 个标签，然后会有一键多值的问题，就只是改了最后一段。  

final_list = []
with open('技术治理-EN-213.jsonl', encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        final_dict = {}
        line = json.loads(line)
        final_dict['text'] = line['text']
        annotations = line['annotations']
        tmp_dict = {}  # 这个是各自的标签对应的句子里标注的词
        for value in map_labels.values():
            tmp_dict[value] = []
        for annotation in annotations:
            start = int(annotation['start_offset'])
            end = int(annotation["end_offset"])
            word = line['text'][start:end]
            tmp_dict[map_labels[annotation['label']]].append(word)
        for label in tmp_dict.keys():
            final_dict[label] = str(tmp_dict[label]).replace('[', '').replace(']', '') if tmp_dict[label] else '' # 去除左右列表符号
        final_list.append(final_dict)
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
        self.data = re.sub(f'({source})', r"<TAG country='{}'>\1</TAG>".format(target), self.data)
        return self
    
    def normalize(self):
        self.data = re.sub(r'[<>=\'\'/ ，]', '', self.data).strip()
        return self


print(TextTools('\t这是一个字符串，有中科院这个单词   ').add_tag(source='中科院', target='中国').normalize())
```



