import json
import logging

import datetime
from collections import defaultdict
from functools import partial

import pandas as pd
import re
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from data_analysis.tools.mx_simhash import compute_simhash
from data_analysis.filters.base import BaseKeyFilter
from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory

from post.models import today, lastday, ZKYYuceEntry_EN, ZKYYuce_EN, ZKYObjects_EN
from user.utils import trans_to_md5

from data_analysis.tools.utils import get_logger
logger = get_logger(__file__)
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-a',
            '--all',
            dest='isall',
            action='store_true',
            help='是否导入全部时间段',
        )
        parser.add_argument(
            '-f',
            '--from',
            dest='from_time',
            default=lastday(time_str='00:00:00',to_datetime_str=True), # 默认从昨天8开始
            help='起始时间，格式 yyyy-MM-dd HH-mm-ss',
        )
        parser.add_argument(
            '-t',
            '--to',
            dest='to_time',
            default=today(time_str='08:00:00',to_datetime_str=True),  # 默认今天8点
            help='结束时间，格式 yyyy-MM-dd HH-mm-ss',
        )
        parser.add_argument(
            '-l',
            '--last',
            dest='last_days',
            type=int,
            help='起始日期为距离今天的天数前的日期"',
        )
        pass

    def handle(self, *args, **options):
        from_date,to_date = None,None
        isall = options.get('isall')
        space_rule = r'[^\S\r\n]+'
        # _,name_id_map = ZKYZhiliKeywords.zhili_map()
        if options['isall']:
            ZKYYuceEntry_EN.objects.all().delete()
            ZKYYuce_EN.objects.all().delete()
        # 优先last参数
        if options.get('last_days',None):
            from_date = lastday(options['last_days'],to_datetime_str=True)
            to_date = today(to_datetime_str=True)
        else:
            from_date = options['from_time']
            to_date = options['to_time']
        obj_mapping = defaultdict(list)
        for main_obj in ZKYObjects_EN.objects.filter(level=3).all():
            # [ [三级ID,三级名,二级ID,一级ID],…… ]
            obj_mapping[main_obj.name].append(main_obj.id)
            obj_mapping[main_obj.name].append(main_obj.name)
            obj_mapping[main_obj.name].append(main_obj.parent.id)
            obj_mapping[main_obj.name].append(main_obj.first_parent.id)
            pass
        # 生成index
        obj_filter = BaseKeyFilter(obj_mapping.keys())
        useful_get = lambda target,key,default=None: default if target.get(key,default) is None else target.get(key,default)
        for datas in ConnectManager.ES.get_setting('DEBUG').search_by_page_with_searchafter(
            settings.ZKY_EN_YUCE_INDEX,
            doc='yuce_doc',
            query={} if isall else {
                "query":{
                  "bool":{
                      "must": [
                          {
                              "query_string": {
                                  "default_field": "post_time",
                                  "query": f"[\"{from_date}\"  TO \"{to_date}\"]"
                              }
                          }
                      ]
                  }
                }
              },
            sort_fields=[{'post_time':'desc'}],
            fields=['site_name','url','post_time','yuce_text','text','entry_id','flag','title']
        ):
            for data in datas:
                get = partial(useful_get,data)
                try:
                    date = datetime.datetime.strptime(data['post_time'],'%Y-%m-%d %H:%M:%S').date()
                    for keyword in obj_filter.exec_filter(get('title','')+get('text','')): # 遍历字典，因为只有name没有同义词，所以这个是去重的
                        yuce_text_md5 = trans_to_md5(data['yuce_text'])
                        yuce,iscreated = ZKYYuce_EN.objects.get_or_create(
                            yuce_text_md5 = yuce_text_md5,
                            defaults={
                                'url':data['url'],
                                'post_time':data['post_time'],
                                'yuce_text':data['yuce_text'],
                                'text':data['text'],
                                'site_name':data['site_name'],
                                'flag':data['flag'].replace('#','、')
                            }
                        )
                        if iscreated:
                            logger.info(f'预测观点：【{yuce.site_name}】 Created')
                        for entry_id in [obj_mapping[keyword][0],obj_mapping[keyword][2],obj_mapping[keyword][3]]:
                            entry,iscreated = ZKYYuceEntry_EN.objects.get_or_create(post_date=date,object_id=entry_id)
                            entry.save()
                            yuce.entry.add(entry)
                            if iscreated:
                                logger.info(f'\t{keyword} created')
                            else:
                                logger.info(f'\t{keyword} exists')
                        pass
                except Exception as e:
                    print(e)
                    # print(e.with_traceback())
                    continue

            pass
        logger.info(f'完成')
        pass

