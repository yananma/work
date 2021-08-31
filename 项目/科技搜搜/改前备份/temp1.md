```python 
import datetime
import json

from django.conf import settings
from django.db.models import Q, Count

from cache_worker import ZKYCache
from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory
from post.models import ZKYPosts
from search import SearchEnum
from search.search_middleware import SearchMiddleware


class CountryPostsSearchMiddleware(SearchMiddleware):

    def __init__(self,top_level_judge_flag=SearchEnum.NO):
        #self.main_objs_data = CacheMutiplexing.get_or_set_main_objects_top_level_cache()
        self.title_country='titlecountry'
        self.text_country='textcountry'
        super(CountryPostsSearchMiddleware, self).__init__()

    def init_args(self,*args,**kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = super(CountryPostsSearchMiddleware, self).init_args(*args, **kwargs)
        page,size = kwargs.pop('page',1)-1,kwargs.pop('size',10)
        flag = kwargs.pop('flag',0)
        country = kwargs.pop('country_or_region', 'all')
        search_after = json.loads(kwargs.pop('search_after', '[]'))
        return search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag,country,search_after

    def search_until_target_count_post(self, conn, search_after=None, date_range=None, query=None, fields=None,
                                       cache_instance=None, cache_name=None, limit=None, size=10000):
        now_count = 0
        for origin_datas in conn.search_by_page_with_searchafter(
                index=settings.ZKY_INDEX,
                size=size,
                search_after=search_after,
                split_date=True,
                date_range=date_range,
                query=query,
                fields=fields,
                return_all_result=True
        ):
            for post in filter(lambda x: not cache_instance.sismember(cache_name, x['_source']['title_hash']),
                               origin_datas['hits']['hits']):
                yield post['_source'], post['sort']
                now_count += 1
                if now_count >= limit:
                    return

    def trans_posts_to_web_format(self,posts,flag,country):
        """
            对返回的数据进行处理，返回合适的格式
        :param posts:
        :param flag:
        :param country:
        :return:
        """
        country_keyname = 'keyname="' if country=='all' else f'keyname="{country}"'
        if flag==1:
            return [
                {
                    'data':TextFactory(post['title']).replace_countrytag_to_others(self.title_country,source_extra_data=country_keyname,repl_tag=settings.HIGH_LIGHT_TAG,extra_data=settings.HIGH_LIGHT_STYLE).now,
                    'url':post['url'],
                    'post_time':post['post_time']
                }
                for post in posts
            ]
        elif flag==2:
            return [
                {
                    'data': TextFactory(post['text']).chunk_tag_with_max_size_v2(self.text_country,search_flag_str=f'<{self.text_country} {country_keyname}').replace_countrytag_to_others(self.text_country,source_extra_data=country_keyname,repl_tag=settings.HIGH_LIGHT_TAG,extra_data=settings.HIGH_LIGHT_STYLE).now,
                    'url': post['url'],
                    'post_time': post['post_time']
                }
                for post in posts
            ]
        else:
            results=[]
            for post in posts:
                if post['title'].find(f'<{self.title_country} {country_keyname}')!=-1:
                    results.append({
                    'data':TextFactory(post['title']).replace_countrytag_to_others(self.title_country,source_extra_data=country_keyname,repl_tag=settings.HIGH_LIGHT_TAG,extra_data=settings.HIGH_LIGHT_STYLE).now,
                    'url':post['url'],
                    'post_time':post['post_time']
                })
                else:
                    results.append(
                        {
                            'data': TextFactory(post['text']).chunk_tag_with_max_size_v2(self.text_country,search_flag_str=f'<{self.text_country} {country_keyname}').replace_countrytag_to_others(self.text_country, source_extra_data=country_keyname,repl_tag=settings.HIGH_LIGHT_TAG,extra_data=settings.HIGH_LIGHT_STYLE).now,
                            'url': post['url'],
                            'post_time': post['post_time']
                        }
                    )
                pass
            return results

    def db(self,*args,**kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag, country = self.init_args(*args, **kwargs)

        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords, exclude_keywords,search_mode)

        all_posts_cache_name = cache_instance.make_cache_name('country_posts', cache_keywords_name,from_date,to_date, flag,country)
        has_key = cache_instance.exists(all_posts_cache_name)
        if has_key:
            return True,(cache_instance.slice(all_posts_cache_name, page * size, size), cache_instance.len(all_posts_cache_name))


        # # 获取该关键词、该日期下的所有文章
        # all_posts_temp_posts = cache_instance.make_cache_name('country_temp_posts', cache_keywords_name,from_date,to_date,country,flag)

        country_field = 'text_title_country'
        if flag==1:
            country_field = 'title_country'
        elif flag==2:
            country_field = 'text_country'
        if country=='all':
            q_obj = ~Q(**{country_field:''})
        else:
            q_obj = Q(**{f'{country_field}__contains':country})

        filters_list = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not filters_list:
            return False,settings.ERROR_MSG_MAP['NO_CACHE']
        filters = self.deserializer_filters(ZKYPosts.objects, filters_list)
        filters = filters.filter(post_time__lte=to_date,post_time__gte=from_date).filter(q_obj).order_by('-post_time')

        # cache_instance.rpush(all_posts_temp_posts, posts, filter_func=lambda post: TextFactory(post['title']).replace_all_not_word_char_to_null().now)
        all_posts = self.trans_posts_to_web_format([
            {
                'title':post['title'],
                'url': post['url'],
                'text':post['text'],
                'post_time': post['post_time'].strftime('%Y-%m-%d')
            }
            for post in filters.values('title', 'url', 'text', 'post_time')
        ],flag,country)
        cache_instance.rpush(all_posts_cache_name,all_posts,filter_func=lambda post:TextFactory(post['data']).replace_all_not_word_char_to_null().now)

        return True,(cache_instance.slice(all_posts_cache_name,page*size,size),cache_instance.len(all_posts_cache_name))

    def es(self,*args,**kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag, country,search_after = self.init_args(*args, **kwargs)

        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords, exclude_keywords,search_mode)

        all_posts_cache_name = cache_instance.make_cache_name('country_posts', cache_keywords_name,from_date,to_date, flag,country)

        # 缓存名
        search_after_cache_name = cache_instance.make_cache_name('country_posts_search_after_', all_posts_cache_name)
        if cache_instance.exists(search_after_cache_name) or settings.CACHE_DEBUG:
            search_after = cache_instance.get(search_after_cache_name)

        # title_hash的set的缓存名
        title_hash_cache_name = cache_instance.make_cache_name('country_posts_title_hash_', all_posts_cache_name)
        # 文章总数的缓存名
        country_posts_count_cache_name = cache_instance.make_cache_name('country_posts_count_', all_posts_cache_name)
        # 判断总数缓存是否存在，存在直接取，不存在请求
        has_key = cache_instance.exists(all_posts_cache_name, ignore_debug=True)
        if has_key:
            now_post_count = cache_instance.len(all_posts_cache_name)
        else:
            now_post_count = 0
        user_want_min_count = (page + 1) * 10

        if cache_instance.exists(country_posts_count_cache_name, ignore_debug=True):
            has_count_key = True
        else:
            has_count_key = False

        if has_key and has_count_key and user_want_min_count<=now_post_count:
            search_after = json.dumps(search_after)
            all_post_count = cache_instance.get(country_posts_count_cache_name)
            return True,(cache_instance.slice(all_posts_cache_name,page*size,size),all_post_count, search_after)
        conn = ConnectManager.ES.get_setting('DEBUG')
        es_query_dict = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not es_query_dict:
            return False,settings.ERROR_MSG_MAP['NO_CACHE']
        es_query_dict['query']['bool']['must'].append({
            "query_string": {
                "default_field": "post_time",
                "query": f"[\"{from_date} 00:00:00\"  TO \"{to_date} 23:59:59\"]"
            }
        })

        if flag == 1:
            es_field = 'title_country'
        else:
            es_field = 'text_country'

        if country=='all':
            es_filter_dict = {
                "script": {
                  "script": f"doc['{es_field}'].size()>0"
                }
            }
        else:
            es_filter_dict = {
                "match": {
                    es_field: country
                }
            }

        es_query_dict['_source'] = ['title', 'url', 'text', 'post_time','title_hash']
        es_query_dict['sort'] = [{"post_time": "desc"}]
        es_query_dict['query']['bool']['must'].append(es_filter_dict)

        if has_count_key:
            all_post_count = cache_instance.get(country_posts_count_cache_name)
        else:
            # 查总数
            es_query_dict['aggs'] = {
                "count": {
                    "cardinality": {
                        "field": "title_hash"
                    }
                }
            }
            count_result = conn.search(
                index=settings.ZKY_INDEX,
                size=0,
                split_date=True,
                date_range=(from_date, to_date),
                body=es_query_dict,
            )
            all_post_count = count_result['aggregations']['count']['value']
            cache_instance.set(country_posts_count_cache_name,all_post_count)

        rise_count = 100
        limit_count = user_want_min_count + rise_count - now_post_count
        _search_after = search_after
        tmp_globals = {'_search_after': _search_after}
        # results = ConnectManager.ES.get_setting('DEBUG').conn.search(index=settings.ZKY_INDEX, size=10000,
        #                                                              body=es_query_dict)

        all_posts = self.trans_posts_to_web_format([
            (cache_instance.sadd(title_hash_cache_name, post['title_hash']) and False)
            or
            (exec('tmp_globals["_search_after"]=sort', {'tmp_globals': tmp_globals}, locals()))
            or
            {
                'title': post['title'],
                'url': post['url'],
                'text': post['text'],
                'post_time': post['post_time'].split()[0]
            }for post, sort in self.search_until_target_count_post(conn, search_after=search_after or None,
                                                    date_range=(from_date, to_date), query=es_query_dict,
                                                    fields=['title', 'url', 'site_name', 'post_time',
                                                            'title_hash'],
                                                    cache_instance=cache_instance,
                                                    cache_name=title_hash_cache_name,
                                                    limit=limit_count, size=rise_count * 10)
        ], flag, country)

        cache_instance.rpush(all_posts_cache_name,
                             all_posts,
                             filter_func=lambda post: TextFactory(post['data']).replace_all_not_word_char_to_null().now)

        search_after = json.dumps(_search_after)
        # 保存search_after缓存
        cache_instance.set(search_after_cache_name,search_after)
        return True,(cache_instance.slice(all_posts_cache_name, page * size, size), all_post_count, search_after)

```
