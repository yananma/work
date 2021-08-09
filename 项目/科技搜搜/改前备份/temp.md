
```python 
import random

import copy
from django.http import HttpRequest
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

# Create your views here.
from cache_worker import ZKYCache
from post.caches import CacheMutiplexing
from post.globals import objects_map_index
from post.models import today, lastday, ZKYHotPosts, ZKYHotPostsPics, ZKYObjects, ZKYZhiliKeywords
from post.serializers import ZKYHotPostsSerializer, ZKYHotPostsPicSerializer
from data_analysis.models import ZKYCountry
from search import searchMiddleware, countryCountSearchMiddleware, importantSearchMiddleware, \
    countryPostsSearchMiddleware, yucePostsMiddleware, zhiliCountMiddleware, zhiliPostsMiddleware
from user.middlewares import check_login_level


def filter_no_searched_request(*args, **kwargs):
    for arg in args:
        if isinstance(arg, (Request, HttpRequest)):
            request = arg
            break
    include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
    anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
    exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
    search_mode = int(request.GET.get('search_mode') or 1)
    cache_index = ZKYCache('1 08:00:00')
    if cache_index.get_by_args('search_posts',
                               cache_index.make_cache_name('search_args_name', include, anyclude, exclude,
                                                           search_mode)) is None:
        return Response({"status_code": 408, "message": "页面加载卡住了，请您重新搜索关键词"})
    pass


class CacheView(ViewSet):
    @action(methods=['post'], detail=False, url_path='deleteall')
    def clear_all_cache(self, request):
        use_flush_db = int(request.data.get('flushdb', 0))
        if use_flush_db:
            ZKYCache.flushdb()
        else:
            ZKYCache.delete_all()
        return Response({'status_code': 200})

    pass


class HotPostsView(ViewSet):
    serializer_class = ZKYHotPostsSerializer

    @check_login_level()
    @action(methods=['get'], detail=False, url_path='main')
    def main_page(self, request):
        cache_instance = ZKYCache('1 08:00:00')  # 创建缓存实例，可以缓存到明天八点之前
        cache_name = cache_instance.make_cache_name('main_page')  # 利用参数和标识符创建并返回cache名，这里参数为空，要注意参数顺序影响名字
        cache_data = cache_instance.get(cache_name)  # 根据cache名获取缓存内容
        if cache_data:  # 存在缓存的话利用缓存的参数字典来返回对象
            return cache_instance.apply_to_func(Response, cache_data)

        result = {
            "status_code": 200
        }
        result["data"] = self.serializer_class(
            data=ZKYHotPosts.objects.filter(state=ZKYHotPosts.StateChoice.ACTIVE).order_by('-post_time')[:5], many=True)
        result["data"].is_valid()
        result["data"] = result["data"].data
        result["pics"] = []
        for pic_obj in random.sample(
                list(ZKYHotPostsPics.objects.filter(state=ZKYHotPostsPics.StateChoice.ACTIVE).all()),
                k=2
        ):
            result["pics"].append(pic_obj.pic.url)
        return cache_instance(Response)(cache_name, result)  # 这里第一个参数为缓存名，在返回数据的同时创建缓存

    @check_login_level()
    @action(methods=['get'], detail=False, url_path='main/all')
    def all(self, request):
        state = request.GET.get('state', ZKYHotPosts.StateChoice.ACTIVE)
        result_data = self.serializer_class(
            data=ZKYHotPosts.objects.filter(post_time__lt=today(), post_time__gte=lastday(), state=state), many=True)
        result_data.is_valid()
        return Response(result_data.data)

    @check_login_level()
    @action(methods=['get'], detail=False, url_path='main/picall')
    def pic_all(self, request):
        state = request.GET.get('state', ZKYHotPostsPics.StateChoice.ACTIVE)
        #
        cache_instance = ZKYCache('0 16:00:00')
        cache_1_name = cache_instance.make_cache_name('pic_all', state)
        cache_1_data = cache_instance.get(cache_1_name)
        if cache_1_data:
            return cache_instance.apply_to_func(Response, cache_1_data)
        result_data = ZKYHotPostsPicSerializer(data=ZKYHotPostsPics.objects.filter(state=state), many=True)
        result_data.is_valid()
        return cache_instance(Response)(cache_1_name, {"status_code": 200, "data": result_data.data})
        # return Response(result_data.data)

    @check_login_level()
    @action(methods=['get'], detail=False, url_path='main/objects')
    def main_objects(self, request):
        cache_instance = ZKYCache('1 08:00:00')
        cache_result_name = cache_instance.make_cache_name('main_objects_result')
        cache_instance.delete(cache_result_name)
        cache_result_data = cache_instance.get(cache_result_name)
        if cache_result_data:
            return cache_instance.apply_to_func(Response, cache_result_data)

        objects_valus = ZKYObjects.objects.order_by('level', 'sorted_value').values('id', 'name', 'level',
                                                                                    'first_parent__name',
                                                                                    'parent__name', 'pic')
        objects_cache_map = {}
        objects_return_json = []
        for obj_dict in objects_valus:
            cache_map_data = objects_cache_map.get(obj_dict['name'])
            # 不存在或者当前level大于现有的
            if not cache_map_data or obj_dict['level'] < cache_map_data['level']:
                objects_cache_map[obj_dict['name']] = obj_dict
                cache_map_data = obj_dict
            # 前端的数据
            result_obj_dict = copy.deepcopy(obj_dict)
            if obj_dict['level'] == 1:
                result_obj_dict['data'] = []
                objects_return_json.append(result_obj_dict)
            elif obj_dict['level'] == 2:
                result_obj_dict['data'] = []
                for _first_dict in objects_return_json:
                    if _first_dict['name'] == cache_map_data['first_parent__name']:
                        _first_dict['data'].append(result_obj_dict)
                        break
            elif obj_dict['level'] == 3:
                first_dict = None
                for _first_dict in objects_return_json:
                    if _first_dict['name'] == cache_map_data['first_parent__name']:
                        first_dict = _first_dict
                        break
                for _second_dict in first_dict['data']:
                    if _second_dict['name'] == cache_map_data['parent__name']:
                        _second_dict['data'].append(result_obj_dict)
                        break
                pass
            pass
        # 不限时间的缓存
        cache_suggest_instance = ZKYCache('1 08:00:00')
        cache_name = cache_suggest_instance.make_cache_name('main_objects')
        cache_suggest_instance.set(cache_name, objects_cache_map)

        # 关键词map cache
        CacheMutiplexing.get_or_set_objects_map_cache()
        # map_index

        return cache_instance(Response)(cache_result_name, {'status_code': 200, 'data': objects_return_json})

    pass


class SearchView(ViewSet):

    @check_login_level()
    @action(methods=['get'], detail=False, url_path='suggest')
    def suggest(self, request):
        keyword = request.GET.get('keyword')
        cache_index = ZKYCache('1 08:00:00')
        # 先检查suggest缓存是否存在
        suggest_cache_name = cache_index.make_cache_name('suggest', keyword)
        suggest_cache_data = cache_index.get(suggest_cache_name)
        if suggest_cache_data:
            return cache_index.apply_to_func(Response, suggest_cache_data)
        # 不存在的话开始算
        # 获取缓存里的关键字信息
        objects_cache_data = CacheMutiplexing.get_or_set_main_objects_top_level_cache()
        # 获取缓存里的关键词映射数据
        cache_suggest_map_data = CacheMutiplexing.get_or_set_objects_map_cache()
        # 进行suggest筛选
        results = set()
        main_objects_suggests = list(filter(lambda x: keyword.upper() in x.upper(),
                                            {k: v for k, v in objects_cache_data.items() if v['level'] < 3}.keys()))
        results.update(main_objects_suggests)
        # # 把关键词映射数据拼成一句话然后用index搜索
        # for map_obj in objects_map_index().exec_filter('#'.join(main_objects_suggests)):
        #     results.update(map_obj['synonyms'].split(','))
        return cache_index(Response)(suggest_cache_name, {"status_code": 200, "data": list(results)})

    # @check_login_level()
    @action(methods=['get'], detail=False, url_path='count')
    def search(self, request):
        include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
        anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
        exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
        search_mode = int(request.GET.get('search_mode') or 1)
        from_date = request.GET.get('from') or lastday(90, to_date_str=True, time_str='00:00:00')
        to_date = request.GET.get('to') or today(to_date_str=True, time_str='00:00:00')

        cache_index = ZKYCache('1 08:00:00')
        search_name = cache_index.make_cache_name('search_args_name', include, anyclude, exclude, search_mode)

        with_date_search_name = cache_index.make_cache_name('search_with_date', search_name, from_date, to_date)
        search_cache_data = cache_index.get(with_date_search_name)
        if search_cache_data:
            return cache_index.apply_to_func(Response, search_cache_data)

        judge_sucess, msg_or_data_and_mode = searchMiddleware(include_keywords=include, anyclude_keywords=anyclude,
                                                              exclude_keywords=exclude, from_date=from_date,
                                                              to_date=to_date, token=request.token,
                                                              search_mode=search_mode)
        if not judge_sucess:
            return Response({'status_code': msg_or_data_and_mode[0], 'message': msg_or_data_and_mode[1], 'data': []})
        data = msg_or_data_and_mode[0]

        # count = 0
        # for data in msg_or_data:
        #     count+=data['count']
        # print(f'数量：{count}')
        if judge_sucess:
            return cache_index(Response)(search_name, {'status_code': 200, 'data': data, 'message': ''})

    # @check_login_level(filter_func_list=[filter_no_searched_request])
    @action(methods=['get'], detail=False, url_path='country/count')
    def country_counts(self, request):
        include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
        anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
        exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
        search_mode = int(request.GET.get('search_mode') or 1)
        from_date = request.GET.get('from') or lastday(90, to_date_str=True, time_str='00:00:00')
        to_date = request.GET.get('to') or today(to_date_str=True, time_str='00:00:00')

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include, anyclude, exclude, search_mode)
        search_name = cache_index.make_cache_name('search_country_count', search_args_name, from_date, to_date)
        search_contry_cache_data = cache_index.get(search_name)
        if search_contry_cache_data:
            cache_index.apply_to_func(Response, search_contry_cache_data)

        judge_sucess, country_data = countryCountSearchMiddleware(include_keywords=include, anyclude_keywords=anyclude,
                                                                  exclude_keywords=exclude, from_date=from_date,
                                                                  to_date=to_date, token=request.token,
                                                                  search_mode=search_mode)
        if not judge_sucess:
            return Response({'status_code': country_data[0], 'message': country_data[1], 'data': []})
        return cache_index(Response)(search_name, {"status_code": 200, "messgae": "", "data": country_data[0]})

    @check_login_level(filter_func_list=[filter_no_searched_request])
    @action(methods=['get'], detail=False, url_path='importants')
    def important_posts(self, request):
        include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
        anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
        exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
        search_mode = int(request.GET.get('search_mode') or 1)
        from_date = request.GET.get('from') or lastday(90, to_date_str=True, time_str='00:00:00')
        to_date = request.GET.get('to') or today(to_date_str=True, time_str='00:00:00')
        flag = int(request.GET.get('flag') or 0)

        page = int(request.GET.get('page') or 1)
        size = int(request.GET.get('size') or 10)
        if page < 0:
            page = 1

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include, anyclude, exclude, search_mode)
        search_name = cache_index.make_cache_name('important_posts', search_args_name, from_date, to_date, flag, page,
                                                  size)
        important_posts_cache_data = cache_index.get(search_name)
        if important_posts_cache_data:
            cache_index.apply_to_func(Response, important_posts_cache_data)
        judge_sucess, results_and_count = importantSearchMiddleware(include_keywords=include,
                                                                    anyclude_keywords=anyclude,
                                                                    exclude_keywords=exclude, search_mode=search_mode,
                                                                    from_date=from_date, to_date=to_date,
                                                                    token=request.token, page=page, size=size,
                                                                    flag=flag)
        if not judge_sucess:
            return Response({'status_code': results_and_count[0], 'message': results_and_count[1], 'data': []})
        results, count = results_and_count

        return cache_index(Response)(search_name, {"status_code": 200, "messgae": "", "data": results, "count": count})

    # @check_login_level(filter_func_list=[filter_no_searched_request])
    @action(methods=['get'], detail=False, url_path='countries_and_regions/posts')
    def country_posts(self, request):
        include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
        anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
        exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
        search_mode = int(request.GET.get('search_mode') or 1)
        from_date = request.GET.get('from') or lastday(90, to_date_str=True, time_str='00:00:00')
        to_date = request.GET.get('to') or today(to_date_str=True, time_str='00:00:00')
        flag = int(request.GET.get('flag') or 0)

        page = int(request.GET.get('page') or 1)
        size = int(request.GET.get('size') or 10)
        if page < 0:
            page = 1

        country_or_region = request.GET.get('country_or_region') or 'all'

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include, anyclude, exclude, search_mode)
        search_name = cache_index.make_cache_name('country_posts', search_args_name, from_date, to_date,
                                                  flag, page, size, country_or_region)
        country_posts_cache_data = cache_index.get(search_name)
        if country_posts_cache_data:
            cache_index.apply_to_func(Response, country_posts_cache_data)

        judge_sucess, results_and_count = countryPostsSearchMiddleware(include_keywords=include,
                                                                       anyclude_keywords=anyclude,
                                                                       exclude_keywords=exclude,
                                                                       search_mode=search_mode,
                                                                       from_date=from_date, to_date=to_date,
                                                                       token=request.token, page=page, size=size,
                                                                       flag=flag, country_or_region=country_or_region)
        if not judge_sucess:
            return Response({'status_code': results_and_count[0], 'message': results_and_count[1], 'data': []})
        results, count = results_and_count

        return cache_index(Response)(search_name, {"status_code": 200, "messgae": "", "data": results, "count": count})

    @check_login_level()
    @action(methods=['get'], detail=False, url_path='countries_and_regions/all')
    def all_country(self, request):
        cache_index = ZKYCache('1 08:00:00')
        search_name = cache_index.make_cache_name('all_country')
        country_all_cache_data = cache_index.get(search_name)
        if country_all_cache_data:
            cache_index.apply_to_func(Response, country_all_cache_data)
        countrys = ZKYCountry.objects.order_by('level', 'en_name').values_list('name', flat=True)
        return cache_index(Response)(search_name, {"status_code": 200, "message": "", "data": list(countrys)})

    # @check_login_level(filter_func_list=[filter_no_searched_request])
    @action(methods=['get'], detail=False, url_path='yuce/posts')
    def yuce_posts(self, request):
        include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
        anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
        exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
        from_date = request.GET.get('from') or lastday(90, to_date_str=True, time_str='00:00:00')
        to_date = request.GET.get('to') or today(to_date_str=True, time_str='00:00:00')
        search_mode = int(request.GET.get('search_mode') or 1)
        page = int(request.GET.get('page') or 1)
        if page < 0:
            page = 1
        size = int(request.GET.get('size') or 10)

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include, anyclude, exclude, search_mode)
        search_name = cache_index.make_cache_name('yuce_posts', search_args_name, page, size, from_date, to_date)
        yuce_posts_cache_data = cache_index.get(search_name)
        if yuce_posts_cache_data:
            cache_index.apply_to_func(Response, yuce_posts_cache_data)

        judge_sucess, results_and_count = yucePostsMiddleware(include_keywords=include, anyclude_keywords=anyclude,
                                                              exclude_keywords=exclude, search_mode=search_mode,
                                                              token=request.token, page=page, size=size,
                                                              from_date=from_date, to_date=to_date)
        if not judge_sucess:
            return Response({'status_code': results_and_count[0], 'message': results_and_count[1], 'data': []})
        results, count = results_and_count
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
        max_page = count // size + int(bool(count % size))
        now_page = max_page if len(new_results) == 0 else page
        return cache_index(Response)(search_name,
                                     {"status_code": 200, "messgae": "", "data": new_results, "count": count,
                                      "now_page": now_page, "size": size, "has_next": now_page < max_page,
                                      "has_last": now_page > 1, "max_page": max_page})

    @check_login_level(filter_func_list=[filter_no_searched_request])
    @action(methods=['get'], detail=False, url_path='zhili/count')
    def zhili_counts(self, request):
        include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
        anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
        exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
        from_date = request.GET.get('from') or lastday(90, to_date_str=True, time_str='00:00:00')
        to_date = request.GET.get('to') or today(to_date_str=True, time_str='00:00:00')
        search_mode = int(request.GET.get('search_mode') or 1)

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include, anyclude, exclude, search_mode)
        search_name = cache_index.make_cache_name('search_zhili_count', search_args_name, from_date, to_date)
        search_zhili_cache_data = cache_index.get(search_name)
        if search_zhili_cache_data:
            cache_index.apply_to_func(Response, search_zhili_cache_data)

        judge_sucess, zhili_data = zhiliCountMiddleware(include_keywords=include, anyclude_keywords=anyclude,
                                                        exclude_keywords=exclude, search_mode=search_mode,
                                                        from_date=from_date, to_date=to_date, token=request.token)
        if not judge_sucess:
            return Response({'status_code': zhili_data[0], 'message': zhili_data[1], 'data': []})
        return cache_index(Response)(search_name, {"status_code": 200, "messgae": "", "data": zhili_data[0]})

    @check_login_level(filter_func_list=[filter_no_searched_request])
    @action(methods=['get'], detail=False, url_path='zhili/posts')
    def zhili_posts(self, request):
        include = sorted(filter(lambda x: x, request.GET.get('include', '').split(',')))
        anyclude = sorted(filter(lambda x: x, request.GET.get('anyclude', '').split(',')))
        exclude = sorted(filter(lambda x: x, request.GET.get('exclude', '').split(',')))
        from_date = request.GET.get('from') or lastday(90, to_date_str=True, time_str='00:00:00')
        to_date = request.GET.get('to') or today(to_date_str=True, time_str='00:00:00')
        search_mode = int(request.GET.get('search_mode') or 1)
        page = int(request.GET.get('page') or 1)
        if page < 0:
            page = 1
        size = int(request.GET.get('size') or 10)
        ids = request.GET.get('ids') or ''

        cache_index = ZKYCache('1 08:00:00')
        search_args_name = cache_index.make_cache_name('search_args_name', include, anyclude, exclude, search_mode)
        search_name = cache_index.make_cache_name('zhili_posts', search_args_name, page, size, ids, from_date, to_date)
        zhili_posts_cache_data = cache_index.get(search_name)
        if zhili_posts_cache_data:
            cache_index.apply_to_func(Response, zhili_posts_cache_data)

        judge_sucess, results_and_count = zhiliPostsMiddleware(include_keywords=include, anyclude_keywords=anyclude,
                                                               exclude_keywords=exclude, search_mode=search_mode,
                                                               token=request.token, page=page, size=size, ids=ids,
                                                               from_date=from_date, to_date=to_date)
        if not judge_sucess:
            return Response({'status_code': results_and_count[0], 'message': results_and_count[1], 'data': []})
        results, count = results_and_count
        max_page = count // size + int(bool(count % size))
        now_page = max_page if len(results) == 0 else page
        return cache_index(Response)(search_name, {"status_code": 200, "messgae": "", "data": results, "count": count,
                                                   "now_page": now_page, "size": size, "has_next": now_page < max_page,
                                                   "has_last": now_page > 1, "max_page": max_page})

    @check_login_level()
    @action(methods=['get'], detail=False, url_path='zhili/all')
    def all_zhili(self, request):
        cache_index = ZKYCache('1 08:00:00')
        search_name = cache_index.make_cache_name('all_zhili')
        zhili_all_cache_data = cache_index.get(search_name)
        if zhili_all_cache_data:
            cache_index.apply_to_func(Response, zhili_all_cache_data)
        return cache_index(Response)(search_name, {"status_code": 200, "message": "",
                                                   "data": list(ZKYZhiliKeywords.objects.all().values('id', 'name'))})

    pass
```
