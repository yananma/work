import json
import logging

import datetime
from collections import defaultdict
from functools import partial
import pandas as pd
import re
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from httpx import URL

from data_analysis.tools.mx_simhash import compute_simhash
from data_analysis.filters.base import BaseKeyFilter
from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory
from data_analysis.tools.utils import get_logger

from post.models import ZKYObjects, ZKYEntry, ZKYPosts, today, lastday, ZKYEntry_EN, ZKYPosts_EN, ZKYObjects_EN

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
            help='起始日期为距离今天的天数前的日期',
        )
        pass

    def handle(self, *args, **options):
        from_date,to_date = None,None
        isall = options.get('isall')
        space_rule = r'[^\S\r\n]+'

        global_exclude_keywords = ['招聘', ]
        # if options['isall']:
        #     ZKYEntry_EN.objects.all().delete()
        #     ZKYPosts_EN.objects.all().delete()

        # 优先last参数
        if options.get('last_days', None):
            from_date = lastday(options['last_days'], to_datetime_str=True)
            to_date = today(to_datetime_str=True)
        else:
            from_date = options['from_time']
            to_date = options['to_time']
        # 构造基础查询条件
        en_query_dict = {
            "query": {
                "bool": {
                    "must": [
                        {},
                        (
                            {}
                            if options['isall'] else
                            {
                                "range": {
                                    "include_time": {
                                        "gte": from_date,
                                        "lte": to_date
                                    }
                                }
                            }
                        )

                    ]
                }
            }
        }
        # 构造关键词查询方式列表
        obj_mapping = {}
        for main_obj in ZKYObjects_EN.objects.filter(level=3).all():
            # {obj的id:{'info':[三级ID,三级名,二级ID,一级ID],'keyword':obj的名字}}
            obj_mapping[main_obj.id]={
                'info':[main_obj.id,main_obj.name,main_obj.parent.id,main_obj.first_parent.id],
                'keyword':[main_obj.name]
            }
            # obj_mapping[main_obj.id]['query']={
            #     'query':{
            #         "query_string": {
            #             "fields": ["title", "text"],
            #             "query": "({}) NOT ({})".format(
            #                 'OR'.join(f'"{w}"' for w in obj_mapping[main_obj.id]['keyword']),
            #                 'OR'.join(f'"{w}"' for w in global_exclude_keywords)
            #             )
            #         }
            #     }
            # }
            obj_mapping[main_obj.id]['query'] = {
                    "query_string": {
                        "fields": ["title", "text"],
                        "query": "({}) NOT ({})".format(
                            'OR'.join(f'"{w}"' for w in obj_mapping[main_obj.id]['keyword']),
                            'OR'.join(f'"{w}"' for w in global_exclude_keywords)
                        )
                    }
                }

        # 生成index
        useful_get = lambda target, key, default=None: default if target.get(key, default) is None else target.get(key, default)
        for obj_id, obj_dict in obj_mapping.items():
            entry_ids = obj_dict['info']
            en_query_dict["query"]["bool"]["must"][0] = obj_dict['query']
            for datas in ConnectManager.ES.get_setting('DEBUG').search_by_page_with_searchafter(
                settings.ZKY_EN_INDEX,
                query=en_query_dict,
                sort_fields=[{'post_time': 'asc'}, {'include_time': 'asc'}],
                fields=['title', 'text', 'site_name', 'entry_name', 'site_id', 'entry_id', 'author_name', 'title_country',
                        'text_country', 'post_time', 'include_time', 'url', 'domain', 'category', 'domain', 'title_hash',
                        'title_country_range', 'text_country_range', 'media_id']
            ):
                for data in datas:
                    get = partial(useful_get, data)
                    # ZKYPosts.objects.filter().
                    try:
                        date = datetime.datetime.strptime(data['post_time'],'%Y-%m-%d %H:%M:%S').date()
                        country_all = list(filter(bool, set(get('title_country', '').split('#') + get('text_country', '').split('#'))))
                        post, iscreated = ZKYPosts_EN.objects.get_or_create(
                            url=get('url', ''),
                            defaults={
                                'site_id': data['site_id'],
                                'site_name': get('site_name', ''),
                                'entry_id': data['entry_id'],
                                'entry_name': get('entry_name', ''),
                                'author_name': get('author_name', ''),
                                'text': get('text', ''),
                                'domain': URL(get('url', '')).host,
                                'title': get('title', ''),
                                'include_time': str(data['include_time']),
                                'post_time': str(data['post_time']),
                                'title_country': get('title_country', ''),
                                'title_country_range': get('title_country_range', '[]'),
                                'text_country': get('text_country', ''),
                                'text_country_range': get('text_country_range', '[]'),
                                'text_title_country': '#'.join(country_all),
                                'category': get('category', ''),
                                'title_hash': get('title_hash', ''),
                                'media_id': get('media_id', ''),
                            }
                        )
                        if not iscreated:
                            logger.info(f'文章：【{post.title}】 Existed')
                            continue
                        logger.info(f'文章：【{post.title}】 Created')
                        for entry_id in [entry_ids[0], entry_ids[2], entry_ids[3]]:
                            entry, iscreated = ZKYEntry_EN.objects.get_or_create(post_date=date, object_id=entry_id,defaults={'country_count': json.dumps({})})
                            country_json = defaultdict(int, json.loads(entry.country_count))
                            for country in country_all:
                                country_json[country] += 1
                            entry.country_count = json.dumps(country_json)
                            entry.post_count += 1
                            entry.save()
                            post.entry.add(entry)
                            if iscreated:
                                logger.info(f'\t{entry_ids[1]} created')
                            else:
                                logger.info(f'\t{entry_ids[1]} exists')
                    except Exception as e:
                        print(e)
                        # print(e.with_traceback())
                        continue

                pass
        logger.info(f'完成')
        pass

