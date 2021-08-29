import datetime

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
        return search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag,country

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
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag, country = self.init_args(*args, **kwargs)

        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords, exclude_keywords,search_mode)

        all_posts_cache_name = cache_instance.make_cache_name('country_posts', cache_keywords_name,from_date,to_date, flag,country)
        has_key = cache_instance.exists(all_posts_cache_name)
        if has_key:
            return True,(cache_instance.slice(all_posts_cache_name, page * size, size), cache_instance.len(all_posts_cache_name))

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


        es_query_dict['_source'] = ['title', 'url', 'text', 'post_time']
        es_query_dict['sort'] = [{"post_time": "desc"}]
        es_query_dict['query']['bool']['must'].append(es_filter_dict)
        results = ConnectManager.ES.get_setting('DEBUG').conn.search(index=settings.ZKY_INDEX, size=10000,
                                                                     body=es_query_dict)
        all_posts = self.trans_posts_to_web_format([
            {
                'title': post['_source']['title'],
                'url': post['_source']['url'],
                'text': post['_source']['text'],
                'post_time': post['_source']['post_time'].split()[0]
            }for post in results['hits']['hits']
        ], flag, country)

        cache_instance.rpush(all_posts_cache_name, all_posts,
                             filter_func=lambda post: TextFactory(post['data']).replace_all_not_word_char_to_null().now)

        return True,(cache_instance.slice(all_posts_cache_name, page * size, size), cache_instance.len(all_posts_cache_name))
