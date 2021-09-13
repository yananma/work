
```python 
import datetime
from typing import List, Any

from django.conf import settings
from django.db.models import Count

from cache_worker import ZKYCache
from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory
from post.caches import CacheMutiplexing
from post.models import ZKYPosts
from search import SearchJudgeRule, BaseSearchMiddleware


class SearchMiddleware(BaseSearchMiddleware):
    rules = [SearchJudgeRule]

    def __init__(self):
        self.main_objs_data = CacheMutiplexing.get_or_set_main_objects_top_level_cache()
        super(SearchMiddleware, self).__init__()

    def groupby_in_and_notin(self, iter, intarget_iter):
        in_list, notin_list = [], []
        for it in iter:
            if it in intarget_iter:
                in_list.append(it)
            else:
                notin_list.append(it)
        return in_list, notin_list

    def trans_name_to_id(self, keywords):
        return [self.main_objs_data[keyword]['id'] for keyword in keywords]

    def reduce_func(self, source_obj, func_name, args_func, args):
        """
            函数链式调用
            reduce_func(ZKYPosts.objects,'filter',lambda x:Q(entry__object_id=x),include_keywords_in)
        :param source_obj:
        :param func_name:
        :param args_func:
        :param args:
        :return:
        """
        result_reduce = source_obj
        for arg in args:
            result_reduce = getattr(result_reduce, func_name)(args_func(arg))
        return result_reduce

    def init_args(self, *args, **kwargs):
        include_keywords = sorted(kwargs.pop('include_keywords', []))
        anyclude_keywords = sorted(kwargs.pop('anyclude_keywords', []))
        exclude_keywords = sorted(kwargs.pop('exclude_keywords', []))
        search_mode = kwargs.pop('search_mode', 1)

        from_date = kwargs.pop('from_date')
        to_date = kwargs.pop('to_date')
        token = kwargs.pop('token')
        return search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token

    def deserializer_filters(self, filters, filters_exec_list: List):
        local_dict = locals().copy()
        for row in filters_exec_list:
            exec(row['str'].format(*row['params']), globals(), local_dict)
        return local_dict['filters']

    def db(self, *args, **kwargs) -> Any:
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(
            *args, **kwargs)
        if len(include_keywords) < 1:
            return False, settings.ERROR_MSG_MAP['NO_DB_KEYWORD']
        # include_keywords_in,include_keywords_notin = self.groupby_in_and_notin(include_keywords,self.main_objs_data.keys())
        # anyclude_keywords_in,anyclude_keywords_notin = self.groupby_in_and_notin(anyclude_keywords,self.main_objs_data.keys())
        # exclude_keywords_in,exclude_keywords_notin = self.groupby_in_and_notin(exclude_keywords,self.main_objs_data.keys())

        cache_index = ZKYCache('1 08:00:00')
        # 创建参数md5名
        search_args_name = cache_index.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                       exclude_keywords, search_mode)
        # # 这里的大块注释都是判断是否能进行快速搜索和构建查询的，不过现在不需要了，通过search_mode来判断使用什么query，以及db搜索就是简单的只查一个
        # 通过token存入。之后的指令通过token拿到md5名，这个名字是通用的，后续的缓存也都会用这个来做标识符，这样可以多用户通用
        # search_mode_name = cache_index.make_cache_name('search_db_mode',search_args_name)
        #
        # # 查询是否可以进行快速搜索
        # if not (exclude_keywords or include_keywords_notin or anyclude_keywords_notin):
        #     if (not anyclude_keywords_in and include_keywords_in) or (not include_keywords_in and anyclude_keywords_in):
        #         keywords = anyclude_keywords_in or include_keywords_in
        #         keywords_in_id_map = {}
        #         for k_name in keywords:
        #             if self.main_objs_data[k_name]['level'] == 1:
        #                 for k, v in keywords_in_id_map.items():
        #                     if v['level'] > 1 and v['first_parent_id'] == self.main_objs_data[k_name]['id']:
        #                         del keywords_in_id_map[k]
        #                         keywords_in_id_map[k_name] = self.main_objs_data[k_name]
        #             elif self.main_objs_data[k_name]['level'] == 2:
        #                 for k, v in keywords_in_id_map.items():
        #                     if v['level'] == 1 and self.main_objs_data[k_name]['first_parent_id'] == v['id']:
        #                         break
        #                     elif v['level'] == 3 and v['parent_id'] == self.main_objs_data[k_name]['id']:
        #                         del keywords_in_id_map[k]
        #                 else:
        #                     keywords_in_id_map[k_name] = self.main_objs_data[k_name]
        #             else:
        #                 for k, v in keywords_in_id_map.items():
        #                     if v['level'] < 3 and (v['id'] == self.main_objs_data[k_name]['parend_id'] or v['id'] ==self.main_objs_data[k_name]['first_parent_id']):
        #                         break
        #                 else:
        #                     keywords_in_id_map[k_name] = self.main_objs_data[k_name]
        #
        #         if not anyclude_keywords_in and include_keywords_in:
        #             if len(keywords_in_id_map.keys())==1:
        #                 cache_index.set(search_mode_name,{"mode":'include',"params":list(keywords_in_id_map.values())[0]['id']})
        #             else:
        #                 cache_index.set(search_mode_name,{"mode": 'no', "params": {}})
        #             pass
        #         elif not include_keywords_in and anyclude_keywords_in:
        #             cache_index.set(search_mode_name, {"mode": 'anyclude', "params": list(keywords_in_id_map.values())})
        #         else:
        #             cache_index.set(search_mode_name, {"mode": 'no', "params": {}})
        #     else:
        #         cache_index.set(search_mode_name, {"mode": 'no', "params": {}})
        # else:
        #     cache_index.set(search_mode_name, {"mode": 'no', "params": {}})
        #
        #
        #

        filters = ZKYPosts.objects
        filter_cache_json = []
        # if include_keywords_in:
        #     include_keywords_ids_in = self.trans_name_to_id(include_keywords_in)
        #     filter_cache_json.append({
        #         'str':"filters = self.reduce_func(filters,'filter',lambda x:Q(entry__object_id=x),{})",
        #         'params':[include_keywords_ids_in]
        #     })
        #     filters = self.reduce_func(filters,'filter',lambda x:Q(entry__object_id=x),include_keywords_ids_in)
        # if anyclude_keywords_in:
        #     anyclude_keywords_ids_in = self.trans_name_to_id(anyclude_keywords_in)
        #     filter_cache_json.append({
        #         'str':"filters = filters.filter(entry__object_id__in={})",
        #         'params':[anyclude_keywords_ids_in]
        #     })
        #     filters = filters.filter(entry__object_id__in=anyclude_keywords_ids_in)
        # if include_keywords_notin:
        #     filter_cache_json.append({
        #         'str': "filters = self.reduce_func(filters,'filter',lambda x:(Q(text__icontains=x) | Q(title__icontains=x)),{})",
        #         'params': [include_keywords_notin]
        #     })
        #     filters = self.reduce_func(filters,'filter',lambda x:(Q(text__icontains=x) | Q(title__icontains=x)),include_keywords_notin)
        # if anyclude_keywords_notin:
        #     filter_cache_json.append({
        #         'str': "filters = filters.filter(reduce(operator.or_,((Q(text__icontains=anyclude_keyword) | Q(title__icontains=anyclude_keyword)) for anyclude_keyword in {})))",
        #         'params': [anyclude_keywords_notin]
        #     })
        #     filters = filters.filter(reduce(operator.or_,((Q(text__icontains=anyclude_keyword) | Q(title__icontains=anyclude_keyword)) for anyclude_keyword in anyclude_keywords_notin)))
        # if exclude_keywords_notin:
        #     filter_cache_json.append({
        #         'str': "filters = filters.filter(~reduce(operator.or_,((Q(text__icontains=exclude_keyword) | Q(title__icontains=exclude_keyword)) for exclude_keyword in {})))",
        #         'params': [exclude_keywords_notin]
        #     })
        #     filters = filters.filter(~reduce(operator.or_,((Q(text__icontains=exclude_keyword) | Q(title__icontains=exclude_keyword)) for exclude_keyword in exclude_keywords_notin)))

        # ZKYPosts.objects.filter(entry__post_date__lt=)
        include_keywords_ids = self.trans_name_to_id(include_keywords)
        filters = filters.filter(entry__object_id=include_keywords_ids[0])
        filter_cache_json.append({
            'str': "filters = filters.filter(entry__object_id={})",
            'params': [include_keywords_ids[0]]
        })
        filters = filters.order_by('entry__post_date')
        filter_cache_json.append({
            'str': "filters = filters.order_by('entry__post_date')",
            'params': []
        })
        # if exclude_keywords_in:
        #     filter_cache_json.append({
        #         'str': "filters = filters.exclude(entry__object_id__in=self.trans_name_to_id({}))",
        #         'params': [exclude_keywords_in]
        #     })
        #     filters = filters.exclude(entry__object_id__in=self.trans_name_to_id(exclude_keywords_in))

        cache_index.set_by_args('search_posts', filter_cache_json, search_args_name)

        # # 测试代码
        # for post in filters.filter(Q(entry__post_date__lt=to_date) & Q(entry__post_date__gte=from_date)).values('title','text','url','site_name'):
        #     print(f"""
        #     【标题】{post['title']}
        #     【正文】{post['text']}
        #     【连接】{post['url']}
        #     【网站名】{post['site_name']}
        #     """)

        filters = filters.filter(post_time__lte=to_date, post_time__gte=from_date).values('entry__post_date').annotate(
            counts=Count('id'))
        result_counts = []
        start_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        one_day = datetime.timedelta(days=1)
        while start_date <= end_date:
            result_counts.append({'date': start_date.strftime('%Y-%m-%d'), 'count': 0})
            start_date = start_date + one_day
        for has_count_date in filters:
            result_counts[-1 - (end_date - has_count_date['entry__post_date']).days]['count'] = has_count_date['counts']

        return True, (result_counts,)

    def es(self, *args, **kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(
            *args, **kwargs)

        def join_query_str(keywords: List, join_word: str, prefix=''):
            # join_str = join_word.join(f' "{keyword}" ' for keyword in keywords)
            join_str = join_word.join(f' "{TextFactory(keyword).replace_all_not_word_char_to_null().now}" ' for keyword in keywords)
            if join_str:
                return f'{prefix} ({join_str})'
            else:
                return ''

        es_query_dict = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "fields": ["text", "title"],
                                "default_operator": "AND",
                                "query": f"{join_query_str(anyclude_keywords, 'OR')}{join_query_str(include_keywords, 'AND', prefix=' AND ' if anyclude_keywords else '')}{join_query_str(exclude_keywords, 'OR', prefix=' NOT ')}"
                            }
                        },
                        {
                            "bool": {
                                "must_not": [
                                    {
                                        "prefix": {
                                            "entry_name.keyword": {
                                                "value": "知乎"
                                            }
                                        }
                                    },
                                    {
                                        "prefix": {
                                            "entry_name": "知乎"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                       exclude_keywords, search_mode)
        # 通过token存入。之后的指令通过token拿到md5名，这个名字是通用的，后续的缓存也都会用这个来做标识符，这样可以多用户通用
        # cache_index.set_by_args('search_args_name', cache_keywords_name, token)
        cache_index.set_by_args('search_posts', es_query_dict, search_args_name)
        es_query_dict.update(
            {
                'aggs': {
                    "zky_date_group": {
                        "date_histogram": {
                            "field": "post_time",
                            "interval": "day"
                        }
                    }
                }
            }
        )
        es_query_dict['query']['bool']['must'].append({
            "query_string": {
                "default_field": "post_time",
                "query": f"[\"{from_date} 00:00:00\"  TO \"{to_date} 23:59:59\"]"
            }
        })
        data_result = ConnectManager.ES.get_setting('DEBUG').conn.search(index=settings.ZKY_INDEX, size=0,
                                                                         body=es_query_dict)
        result = []
        now_bucket_index = 0
        buckets = data_result['aggregations']['zky_date_group']['buckets']
        start_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        one_day = datetime.timedelta(days=1)
        while start_date <= end_date:
            if now_bucket_index < len(buckets):
                now_date_str = buckets[now_bucket_index]['key_as_string'].split()[0]
                if now_date_str == start_date.strftime('%Y-%m-%d'):
                    result.append({'date': now_date_str, 'count': buckets[now_bucket_index]['doc_count']})
                    now_bucket_index += 1
                else:
                    result.append({'date': start_date.strftime('%Y-%m-%d'), 'count': 0})
            else:
                result.append({'date': start_date.strftime('%Y-%m-%d'), 'count': 0})
            start_date = start_date + one_day

        return True, (result,)


    def en_db(self, *args, **kwargs) -> Any:
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(
            *args, **kwargs)
        if len(include_keywords) < 1:
            return False, settings.ERROR_MSG_MAP['NO_DB_KEYWORD']

        cache_index = ZKYCache('1 08:00:00')
        # 创建参数md5名
        search_args_name = cache_index.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                       exclude_keywords, search_mode)

        filters = ZKYPosts.objects
        filter_cache_json = []

        include_keywords_ids = self.trans_name_to_id(include_keywords)
        filters = filters.filter(entry__object_id=include_keywords_ids[0])
        filter_cache_json.append({
            'str': "filters = filters.filter(entry__object_id={})",
            'params': [include_keywords_ids[0]]
        })
        filters = filters.order_by('entry__post_date')
        filter_cache_json.append({
            'str': "filters = filters.order_by('entry__post_date')",
            'params': []
        })

        cache_index.set_by_args('search_posts', filter_cache_json, search_args_name)

        filters = filters.filter(post_time__lte=to_date, post_time__gte=from_date).values('entry__post_date').annotate(
            counts=Count('id'))
        result_counts = []
        start_date = datetime.datetime.strptime(from_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(to_date, '%Y-%m-%d').date()
        one_day = datetime.timedelta(days=1)
        while start_date <= end_date:
            result_counts.append({'date': start_date.strftime('%Y-%m-%d'), 'count': 0})
            start_date = start_date + one_day
        for has_count_date in filters:
            result_counts[-1 - (end_date - has_count_date['entry__post_date']).days]['count'] = has_count_date['counts']

        return True, (result_counts,)

    def en_es(self, *args, **kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(*args, **kwargs)

        def join_query_str(keywords: List, join_word: str, prefix=''):
            join_str = join_word.join(f' "{TextFactory(keyword).replace_all_not_word_char_to_null().now}" ' for keyword in keywords)
            if join_str:
                return f'{prefix} ({join_str})'
            else:
                return ''

        es_query_dict = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "fields": ["text", "title"],
                                "default_operator": "AND",
                                "query": f"{join_query_str(anyclude_keywords, 'OR')}{join_query_str(include_keywords, 'AND', prefix=' AND ' if anyclude_keywords else '')}{join_query_str(exclude_keywords, 'OR', prefix=' NOT ')}"
                            }
                        }
                    ]
                }
            }
        }

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                       exclude_keywords, search_mode)
        # 通过token存入。之后的指令通过token拿到md5名，这个名字是通用的，后续的缓存也都会用这个来做标识符，这样可以多用户通用
        # cache_index.set_by_args('search_args_name', cache_keywords_name, token)
        cache_index.set_by_args('search_posts', es_query_dict, search_args_name)
        es_query_dict.update(
            {
                'aggs': {
                    "zky_date_group": {
                        "date_histogram": {
                            "field": "post_time",
                            "interval": "day"
                        }
                    }
                }
            }
        )
        es_query_dict['query']['bool']['must'].append({
            "query_string": {
                "default_field": "post_time",
                "query": f"[\"{from_date} 00:00:00\"  TO \"{to_date} 23:59:59\"]"
            }
        })
        data_result = ConnectManager.ES.get_setting('DEBUG').conn.search(index=settings.ZKY_EN_INDEX, size=0,
                                                                         body=es_query_dict)
        result = []
        now_bucket_index = 0
        buckets = data_result['aggregations']['zky_date_group']['buckets']
        start_date = datetime.datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(to_date, '%Y-%m-%d')
        one_day = datetime.timedelta(days=1)
        while start_date <= end_date:
            if now_bucket_index < len(buckets):
                now_date_str = buckets[now_bucket_index]['key_as_string'].split()[0]
                if now_date_str == start_date.strftime('%Y-%m-%d'):
                    result.append({'date': now_date_str, 'count': buckets[now_bucket_index]['doc_count']})
                    now_bucket_index += 1
                else:
                    result.append({'date': start_date.strftime('%Y-%m-%d'), 'count': 0})
            else:
                result.append({'date': start_date.strftime('%Y-%m-%d'), 'count': 0})
            start_date = start_date + one_day

        return True, (result,)
```
