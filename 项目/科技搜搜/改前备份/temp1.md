
import datetime

from django.conf import settings
from django.db.models import Q, Count

from cache_worker import ZKYCache
from data_analysis.connect import ConnectManager
from data_analysis.tools.text_tools import TextFactory
from post.models import ZKYPosts
from search import SearchEnum
from search.search_middleware import SearchMiddleware

class ImportantPostsSearch(SearchMiddleware):


    def __init__(self,top_level_judge_flag=SearchEnum.NO):
        #self.main_objs_data = CacheMutiplexing.get_or_set_main_objects_top_level_cache()
        super(ImportantPostsSearch, self).__init__()

    # def init_args(self,*args,**kwargs):
    #     include_keywords = sorted(kwargs.pop('include_keywords', []))
    #     anyclude_keywords = sorted(kwargs.pop('anyclude_keywords', []))
    #     exclude_keywords = sorted(kwargs.pop('exclude_keywords', []))
    #     from_date = datetime.datetime.strptime(kwargs.pop('from_date'), '%Y-%m-%d').date()
    #     to_date = datetime.datetime.strptime(kwargs.pop('to_date'), '%Y-%m-%d').date()
    #     token = kwargs.pop('token')
    #     return include_keywords, anyclude_keywords, exclude_keywords,from_date,to_date,token

    def init_args(self,*args,**kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token = super(ImportantPostsSearch, self).init_args(*args, **kwargs)
        page,size = kwargs.pop('page',1)-1,kwargs.pop('size',10)
        flag = kwargs.pop('flag',0)
        return search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag



    def db(self,*args,**kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag = self.init_args(*args, **kwargs)
        # from_datetime, to_datetime = datetime.datetime.combine(from_date,datetime.time()),datetime.datetime.combine(to_date,datetime.time())

        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords, exclude_keywords,search_mode)


        all_posts_cache_name = cache_instance.make_cache_name('important_posts',cache_keywords_name,from_date,to_date,flag)
        has_key = cache_instance.cache_connect.exists(all_posts_cache_name)
        if has_key:
            return True,(cache_instance.slice(all_posts_cache_name,page*size,size),cache_instance.len(all_posts_cache_name))


        if flag==0:
            q_obj = Q(important=True)
        elif flag==1:
            q_obj = Q(regulatory=True)
        else:
            q_obj = Q(central=True)
        filters_list = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not filters_list:
            return False,settings.ERROR_MSG_MAP['NO_CACHE']
        filters = self.deserializer_filters(ZKYPosts.objects, filters_list)
        filters = filters.filter(post_time__lte=to_date,post_time__gte=from_date).filter(q_obj).order_by('-post_time')

        posts = [
            {
                'title':TextFactory(post['title']).replace_tag_to_others().now,
                'url':post['url'],
                'site_name':post['site_name'],
                'post_time':post['post_time'].strftime('%Y-%m-%d')
            } for post in filters.values('title','url','site_name','post_time')
        ]
        cache_instance.rpush(all_posts_cache_name,posts,filter_func=lambda post:TextFactory(post['title']).replace_all_not_word_char_to_null().now)
        return True,(cache_instance.slice(all_posts_cache_name,page*size,size),cache_instance.len(all_posts_cache_name))

    def es(self,*args,**kwargs):
        search_mode, include_keywords, anyclude_keywords, exclude_keywords, from_date, to_date, token, page, size, flag = self.init_args(*args, **kwargs)

        cache_instance = ZKYCache('1 08:00:00')
        cache_keywords_name = cache_instance.make_cache_name('search_args_name', include_keywords, anyclude_keywords, exclude_keywords,search_mode)

        all_posts_cache_name = cache_instance.make_cache_name('important_posts',cache_keywords_name,from_date,to_date,flag)
        has_key = cache_instance.cache_connect.exists(all_posts_cache_name)
        if has_key:
            return True,(cache_instance.slice(all_posts_cache_name,page*size,size),cache_instance.len(all_posts_cache_name))

        es_query_dict = cache_instance.get_by_args('search_posts', cache_keywords_name)
        if not es_query_dict:
            return False,settings.ERROR_MSG_MAP['NO_CACHE']
        es_query_dict['query']['bool']['must'].append({
            "query_string": {
                "default_field": "post_time",
                "query": f"[\"{from_date} 00:00:00\"  TO \"{to_date} 23:59:59\"]"
            }
        })
        if flag==0:
            filter_dict = {
                "bool":{
                    "should":[
                        {
                            "term":{
                                "central": {
                                    "value": True
                                }
                            }
                        },
                        {
                            "term": {
                                "regulatory": {
                                    "value": True
                                }
                            }
                        }
                    ]
                }
            }
        elif flag==1:
            filter_dict = {
                "term": {
                    "regulatory": {
                        "value": True
                    }
                }
            }
        else:
            filter_dict = {
                "term": {
                    "central": {
                        "value": True
                    }
                }
            }
            pass
        es_query_dict['_source']=['title','url','site_name','post_time']
        es_query_dict['sort']=[{"post_time":"desc"}]
        es_query_dict['query']['bool']['must'].append(filter_dict)
        print(es_query_dict)
        results = ConnectManager.ES.get_setting('DEBUG').conn.search(index=settings.ZKY_INDEX, size=10000, body=es_query_dict)

        char_translate = str.maketrans({i: '' for i in
                                        r"""!"#$%｜&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！～＠＃％＾＊【】（）、。：；’／
                                        ＼＿－＝☆★○●◎◇◆□€■△▲※→←↑↓¤♂♀〖〗『』」「‖〃‘……￥·"""})
        removed_duplicates_result = set()
        new_results = []
        for result in results:
            d = {}
            title = result["text"].translate(char_translate)
            if title not in removed_duplicates_result:
                removed_duplicates_result.add(title)
            else:
                continue
            d["text"] = result["text"]
            d['url'] = result["url"]
            d['author'] = result["author"]
            d["flag"] = result["flag"]
            new_results.append(d)

        cache_instance.rpush(
            all_posts_cache_name,
            [
                {
                    'title':TextFactory(post['_source']['title']).replace_tag_to_others().__str__(),
                    'url':post['_source']['url'],
                    'site_name':post['_source']['site_name'],
                    'post_time':post['_source']['post_time'].split()[0]
                } for post in results['hits']['hits']
            ],
            filter_func=lambda post:TextFactory(post['title']).replace_all_not_word_char_to_null().now
        )

        return True,(cache_instance.slice(all_posts_cache_name,page*size,size),cache_instance.len(all_posts_cache_name))
