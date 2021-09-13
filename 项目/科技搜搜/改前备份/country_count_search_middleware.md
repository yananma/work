```python 
from collections import Counter

from django.conf import settings

from cache_worker import ZKYCache
from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory
from data_analysis.tools.utils import JSON
from post.caches import CacheMutiplexing
from post.models import ZKYPosts
from search.search_middleware import SearchMiddleware
from search.search_module import SearchEnum


class CountrySearchMiddleware(SearchMiddleware):

    def __init__(self, top_level_judge_flag=SearchEnum.NO):
        self.main_objs_data = CacheMutiplexing.get_or_set_main_objects_top_level_cache()
        super(CountrySearchMiddleware, self).__init__()

    def db(self, *args, **kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(
            *args, **kwargs)

        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                             exclude_keywords, search_mode)

        all_country_counter = Counter({"中国": 0, "美国": 0, "加拿大": 0, "日本": 0, "俄罗斯": 0})
        title_set = set()

        filters_list = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not filters_list:
            return False, settings.ERROR_MSG_MAP['NO_CACHE']

        filters = self.deserializer_filters(ZKYPosts.objects, filters_list)
        # 查全部相关文章
        for text_title_country, title in filters.filter(post_time__gte=from_date, post_time__lte=to_date).values_list(
                'text_title_country', 'title'):
            trip_str = TextFactory(title).replace_all_not_word_char_to_null().now
            if trip_str not in title_set:
                all_country_counter.update(filter(lambda x: x, text_title_country.split('#')))
            title_set.add(trip_str)

        all_country_counter['中国'] = all_country_counter['中国大陆'] + all_country_counter['中国台湾'] + all_country_counter[
            '中国香港'] + all_country_counter['中国澳门']
        del all_country_counter['中国大陆'], all_country_counter['中国台湾'], all_country_counter['中国香港'], all_country_counter[
            '中国澳门']
        return True, (
        [{'name': k, 'value': v} for k, v in filter(lambda x: x[1] > 0, all_country_counter.most_common(5))],)

    def es(self, *args, **kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(
            *args, **kwargs)
        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                             exclude_keywords, search_mode)
        # if cache_keywords_name is None:
        #     return "搜索缓存已失效，请重新搜索"
        es_query_dict = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not es_query_dict:
            return False, settings.ERROR_MSG_MAP['NO_CACHE']
        es_query_dict['query']['bool']['must'].append({
            "query_string": {
                "default_field": "post_time",
                "query": f"[\"{from_date} 00:00:00\"  TO \"{to_date} 23:59:59\"]"
            }
        })
        # es_query_dict['query']['bool']['must'].append({
        #     "script": {
        #         "script": "((doc[\"title_country\"].size()>0)||(doc[\"text_country\"].size()>0))"
        #     }
        # })
        es_query_dict['aggs'] = {
            "country_terms": {
                "terms": {
                    "field": "title_text_country",
                    "size": 245
                },
                "aggs": {
                    "single_title": {
                        "cardinality": {
                            "field": "title_hash"
                        }
                    }
                }
            }
        }
        count_datas = ConnectManager.ES.get_setting('DEBUG').search(
            index=settings.ZKY_INDEX,
            body=es_query_dict,
            size=0
        )
        json_datas = JSON(count_datas)
        prfix_tuple = 'aggregations', 'country_terms', 'buckets', ...
        counter = Counter(dict(zip(
            json_datas.__getitem__(prfix_tuple + ('key',)),
            json_datas.__getitem__(prfix_tuple + ('single_title', 'value',)),
        )))
        counter['中国'] = counter['中国大陆'] + counter['中国台湾'] + counter['中国香港'] + counter['中国澳门']
        # es_query_dict['_source']=["title"],
        # title_set = set()
        # # print(es_query_dict)
        # country_count_dict = Counter({"中国":0,"美国":0,"加拿大":0,"日本":0,"俄罗斯":0})
        # for data_result in ConnectManager.ES.get_setting('DEBUG').search_by_page_with_searchafter(index=settings.ZKY_INDEX,query=es_query_dict,fields=['title','title_country','text_country']):
        #     for data in data_result:
        #         title_text_set = set()
        #         if data['title_country']:
        #             title_text_set.update(data['title_country'].split('#'))
        #         if data['text_country']:
        #             title_text_set.update(data['text_country'].split('#'))
        #         title_without_char = TextFactory(data['title']).replace_all_not_word_char_to_null().now
        #         if title_without_char not in title_set:
        #             country_count_dict.update(title_text_set)
        #         title_set.add(title_without_char)
        # country_count_dict['中国']=country_count_dict['中国大陆'] + country_count_dict['中国台湾'] + country_count_dict['中国香港'] + country_count_dict['中国澳门']
        # del country_count_dict['中国大陆'], country_count_dict['中国台湾'], country_count_dict['中国香港'], country_count_dict['中国澳门']
        del counter['中国大陆'], counter['中国台湾'], counter['中国香港'], counter['中国澳门']
        return True, ([{'name': k, 'value': v} for k, v in filter(lambda x: x[1] > 0, counter.most_common(5))],)

    def en_db(self, *args, **kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(
            *args, **kwargs)

        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                             exclude_keywords, search_mode)

        all_country_counter = Counter({"China": 0, "United States": 0, "Canada": 0, "Japan": 0, "Russia": 0})
        title_set = set()

        filters_list = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not filters_list:
            return False, settings.ERROR_MSG_MAP['NO_CACHE']

        filters = self.deserializer_filters(ZKYPosts.objects, filters_list)
        # 查全部相关文章
        for text_title_country, title in filters.filter(post_time__gte=from_date, post_time__lte=to_date).values_list(
                'text_title_country', 'title'):
            trip_str = TextFactory(title).replace_all_not_word_char_to_null().now
            if trip_str not in title_set:
                all_country_counter.update(filter(lambda x: x, text_title_country.split('#')))
            title_set.add(trip_str)

        all_country_counter['China'] = all_country_counter['China'] + all_country_counter['Taiwan (China)'] + all_country_counter[
            'Hong Kong (China)'] + all_country_counter['Macao (China)']
        del all_country_counter['China'], all_country_counter['Taiwan (China)'], all_country_counter['Hong Kong (China)'], all_country_counter[
            'Macao (China)']
        return True, ([{'name': k, 'value': v} for k, v in filter(lambda x: x[1] > 0, all_country_counter.most_common(5))],)

    def en_es(self, *args, **kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = self.init_args(*args, **kwargs)
        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords,
                                                             exclude_keywords, search_mode)
        # if cache_keywords_name is None:
        #     return "搜索缓存已失效，请重新搜索"
        es_query_dict = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not es_query_dict:
            return False, settings.ERROR_MSG_MAP['NO_CACHE']
        es_query_dict['query']['bool']['must'].append({
            "query_string": {
                "default_field": "post_time",
                "query": f"[\"{from_date} 00:00:00\"  TO \"{to_date} 23:59:59\"]"
            }
        })
        es_query_dict['aggs'] = {
            "country_terms": {
                "terms": {
                    "field": "title_text_country",
                    "size": 245
                },
                "aggs": {
                    "single_title": {
                        "cardinality": {
                            "field": "title_hash"
                        }
                    }
                }
            }
        }
        count_datas = ConnectManager.ES.get_setting('DEBUG').search(
            index=settings.ZKY_EN_INDEX,
            body=es_query_dict,
            size=0
        )
        json_datas = JSON(count_datas)
        prfix_tuple = 'aggregations', 'country_terms', 'buckets', ...
        counter = Counter(dict(zip(
            json_datas.__getitem__(prfix_tuple + ('key',)),
            json_datas.__getitem__(prfix_tuple + ('single_title', 'value',)),
        )))
        counter['China'] = counter['China'] + counter['Taiwan (China)'] + counter['Hong Kong (China)'] + counter['Macao (China)']
        del counter['China'], counter['Taiwan (China)'], counter['Hong Kong (China)'], counter['Macao (China)']
        return True, ([{'name': k, 'value': v} for k, v in filter(lambda x: x[1] > 0, counter.most_common(5))],)

```
