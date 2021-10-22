import datetime
import json
import re
import traceback
from collections import namedtuple
from itertools import chain, zip_longest

import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand
from httpx import URL

from data_analysis.connect import ConnectManager
from data_analysis.filters import BaseKeyFilter
from data_analysis.filters.index import ReIndexNode
from data_analysis.models import ZKYCountry, ZKYDataVersion, ZKYSite
from data_analysis.piplines.es_bluk_module import ESBulk
from data_analysis.piplines.es_craw_module import ESSpider
from data_analysis.piplines.lac_module import ZJPointToESLineModule
from data_analysis.tools.data_pipline import DataPipline
from data_analysis.tools.text_tools import reverse_keyfilter_result, TextFactory
from data_analysis.tools.utils import get_logger
from post.models import today, lastday, ZKYRegulatoryObjects, ZKYCentralUrls, ZKYRegulatoryUrls
from user.utils import trans_to_md5

# from pyhanlp import HanLP


logger = get_logger(__file__)
DEBUG = False


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            dest='index',
            default='kejisousou-formal',
            help='插入到的ES的索引',
        )
        parser.add_argument(
            '-pi',
            dest='point_index',
            default='kejisousou-points-formal',
            help='插入到专家观点的ES的索引',
        )
        parser.add_argument(
            '-d',
            dest='doc',
            default='zky_doc',
            help='插入到的ES的文档名字',
        )
        parser.add_argument(
            '-f',
            dest='from',
            default='2020-01-01 00:00:00',
            help='起始日期',
        )
        parser.add_argument(
            '-t',
            dest='to',
            default=today(to_datetime_str=True),
            help='结束日期',
        )
        parser.add_argument(
            '-tp',
            type=int,
            dest='type',
            default=0,
            help='数据类型。0：作者名（但是有域名范围限制），1：链接，2：media_id，3：entry_id，4: 全部数据，用于跑历史数据',
        )
        parser.add_argument(
            '-file',
            dest='file',
            default=settings.RESOURCE_ROOT / 'docs' / 'program' / '科技搜搜V3.0中文数据源.xlsx',
            help='数据规则配置文件',
        )
        parser.add_argument(
            '-max',
            dest='max',
            type=int,
            default=None,
            help='（fi和ti都不存在时生效）该变量中列表的最大分割段数',
        )
        parser.add_argument(
            '-chunk',
            dest='chunk',
            type=int,
            default=None,
            help='（fi和ti都不存在时生效）在当前分割的段数里的第几段',
        )
        parser.add_argument(
            '-fi',
            dest='fi',
            type=int,
            default=None,
            help='从第i项开始',
        )
        parser.add_argument(
            '-ti',
            dest='ti',
            type=int,
            default=None,
            help='在第下标i项结束，不包含关系',
        )
        parser.add_argument(
            '-vs',
            dest='version',
            default=None,
            help='版本名，指定了的话会覆盖自动创建的版本名',
        )
        parser.add_argument(
            '-si',
            dest='sindex',
            default='page,wei,community2',
            help='查询的索引',
        )
        parser.add_argument(
            '-df',
            dest='date_field',
            default='post_time',
            help='查询时根据哪个时间字段进行时间范围限制',
        )
        parser.add_argument(
            '-l',
            dest='last',
            type=int,
            default=None,
            help='查询几天前的数据',
        )
        parser.add_argument(
            '-us',
            dest='use_sentence_cache',
            default='zky_point_sentence_md5_formal',
            help='句子缓存所用的名字',
        )
        parser.add_argument(
            '-uc',
            dest='use_title_cache',
            default='zky_title_md5_formal',
            help='标题缓存所用的名字',
        )
        parser.add_argument(
            '--no-point',
            dest='no_point',
            action='store_true',
            help='是否不上传数据到专家观点ES',
        )
        parser.add_argument(
            '-en',
            dest='english',
            action='store_true',
            help='是否是英文版',
        )
        parser.add_argument(
            '--debug',
            dest='debug',
            action='store_true',
            help='是否开启DEBUG',
        )

        self.cn_type_list = [
            self.type_0,
            self.type_1,
            self.type_2,
            self.type_3,
            self.type_4,
        ]
        self.en_type_list = [
            self.type_en_0,
        ]

        self.TITLE_COUNTRY_TAG = 'titlecountry'
        self.TEXT_COUNTRY_TAG = 'textcountry'
        pass

    def load_rule_data(self, options):
        """
            读取规则数据
            因为返回数据都是namedtuple，所以可扩展
        :param options: 所传参数
        :return: 返回两个参数，一个data的namedtuple，一个others的namedtuple，第一个是规则数据相关内容，第二个是其他信息相关内容
        """
        logger.info('读取规则数据...')
        result_data_tuple_type = namedtuple('result_data_tuple_type', ['author', 'url', 'media_id', 'entry_id'])
        result_others_tuple_type = namedtuple('result_others_tuple_type',
                                              ["true_media_name_map", 'media_name_map', 'global_black_list', 'title_black_list',
                                               'author_with_sitenames', 'trans_sitenames'])

        sheet_names = ['账号', '域名', '版面', '全局屏蔽词', '标题屏蔽词', '白名单网站', '站点转换表']
        df = pd.read_excel(options['file'], engine='openpyxl', sheet_name=sheet_names)
        temp_list = [df[sheet_name] for sheet_name in sheet_names]

        logger.info('替换规则Nan部分...')
        for i, it in enumerate(temp_list):
            temp_list[i] = it.where(it.notnull(), None).to_dict(orient='records')
        logger.info('提取规则数据...')
        result_others = result_others_tuple_type(
            true_media_name_map={int(it['media_id']): str(it['网站']).strip() for it in temp_list[2]},
            media_name_map={int(it['id']): str(it['网站']).strip() for it in temp_list[2] if it and it['id'] and it['网站'] and it['id'] == it['id']},
            global_black_list=[str(it['屏蔽词']).strip() for it in temp_list[3] if it and it['屏蔽词']],
            title_black_list=[str(it['屏蔽词']).strip() for it in temp_list[4] if it and it['屏蔽词']],
            author_with_sitenames=[it['网站名'] for it in temp_list[5] if it and it['网站名']],
            trans_sitenames=[it['网站名'] for it in temp_list[6] if it and it['网站名']]
        )
        result_data = result_data_tuple_type(
            author=[str(it['账号名称']).strip() for it in temp_list[0] if it and it['账号名称']],
            url=[str(it['链接']).lstrip('https://').lstrip('http://').rstrip('/') for it in temp_list[1] if
                 it and it['链接']],
            media_id=list(result_others.true_media_name_map.keys()),
            # TODO 这里跑完新增数据以后要再改成 media_id
            entry_id=list(result_others.media_name_map.keys())
        )
        return result_data, result_others

    def en_load_rule_data(self, options):
        """
            读取英文规则数据
            因为返回数据都是namedtuple，所以可扩展
        :param options: 所传参数
        :return: 返回一个 data 的 namedtuple
        """
        logger.info('读取英文规则数据...')
        result_data_tuple_type = namedtuple('result_data_tuple_type', ['entry_id'])
        result_others_tuple_type = namedtuple('result_others_tuple_type', ['entry_name_map', 'id_category_map'])

        sheet_names = ['本项目自主抓取', '复用其它项目']
        df = pd.read_excel(options['file'], engine='openpyxl', sheet_name=sheet_names)
        temp_list = [df[sheet_name] for sheet_name in sheet_names]

        logger.info('替换规则Nan部分...')
        for i, it in enumerate(temp_list):
            temp_list[i] = it.where(it.notnull(), None).to_dict(orient='records')

        logger.info('提取英文规则数据...')
        ben_entry_name_map = {int(it['id']): str(it['外文网站名称']).strip() for it in temp_list[0] if it and it['id']
                            and it['进度'] and it['id'] == it['id']}
        fuyong_entry_name_map = {int(it['id']): str(it['外文网站名称']).strip() for it in temp_list[1] if it and it['id']
                             and it['id'] == it['id']}
        result_others = result_others_tuple_type(
            entry_name_map={**ben_entry_name_map,**fuyong_entry_name_map},
            id_category_map={int(it['id']): str(it['备注1']).strip() for it in chain(temp_list[0],temp_list[1]) if it and it['id']
                             and it['备注1'] and it['id'] == it['id']}
        )
        ben_entry_id = [int(it['id']) for it in temp_list[0] if it and it['id'] and it['进度']]
        fuyong_entry_id = [int(it['id']) for it in temp_list[1] if it and it['id']]
        result_data = result_data_tuple_type(
            entry_id=ben_entry_id + fuyong_entry_id
        )
        return result_data, result_others

    def cacl_from_and_to_index(self, options, source_data):
        logger.info('计算数据起始位置...')
        # 计算起始
        from_index = 0
        to_index = len(source_data)
        if options['fi'] or options['ti']:
            from_index = options.get('fi', from_index)
            to_index = options.get('ti', to_index)
        else:
            from_index = int(to_index * (options['chunk'] or 0) / (options['max'] or 1))
            to_index = int(min(to_index * ((options['chunk'] or 0) + 1) / (options['max'] or 1), to_index))
        return from_index, to_index

    def get_or_create_data_version(self, options, **kwargs):
        logger.info('创建DataVersion数据...')
        from_index, to_index = kwargs.get('from_index', 0), kwargs.get('to_index', -1)
        need_data = [
            options["from"],
            options["to"],
            str(options["file"]),
            options["type"],
            from_index,
            to_index,
            options["sindex"],
            options["use_title_cache"],
            options["point_index"],
            options["index"],
        ]
        version_md5 = trans_to_md5(need_data)
        version_origin_str = json.dumps(need_data)
        version_name = options['version'] or f'zky_history_data_v2__{version_md5}'
        data_version, created = ZKYDataVersion.objects.get_or_create(
            version=version_name,
            defaults={
                'setting': '',
                'args': json.dumps({
                    'version': version_origin_str,
                    'from': from_index,
                    'post_sucess': 0,
                    'post_faild': 0,
                    'point_sucess': 0,
                    'point_faild': 0,
                    'keyword': to_index
                })
            }
        )
        version_args_json = json.loads(data_version.args)
        logger.info(f"""【Settings】{version_name}
                    [from_date] {options['from']}
                    [to_date]   {options['to']}
                    [file_path] {options['file']}
                    [type]      {options['type']}
                    [from_index]{from_index}
                    [to_index]  {to_index}
                    [index]  {options['index']}
                    [point_index]  {options['point_index']}
                    [use_title_cache]  {options['use_title_cache']}

                    [searchAfter]{data_version.search_after}

                    [now_index] {version_args_json['from']}
                    [post]      {version_args_json['post_sucess']}-{version_args_json['post_faild']}
                    [point]     {version_args_json['point_sucess']}-{version_args_json['point_faild']}
                    [keyword]   {version_args_json['keyword']}
                """)
        return data_version, version_args_json

    def load_datas(self, options, locals_dict):

        data_version, version_args_json = locals_dict.get('data_version'), locals_dict.get('version_args_json')
        search_after = locals_dict.get('search_after')
        for keyword_index, (keyword, keyword_type) in enumerate(locals_dict['source_data'][version_args_json['from']:locals_dict['to_index']]):
            if keyword_index == 1:
                search_after = []
            logger.info(f'keyword {keyword} is start')

            from_date, to_date = options['from'], options['to']
            version_args_json['keyword'] = keyword
            version_args_json['keyword_type'] = keyword_type
            version_args_json['from'] = keyword_index + version_args_json['from']
            data_version.args = json.dumps(version_args_json)
            data_version.save()

            query_dict = {
                "bool": {
                    "must": [
                        {
                            "range": {
                                options['date_field']: {
                                    "gte": from_date,
                                    "lt": to_date
                                }
                            }
                        }
                    ]
                }
            }
            query_dict['bool']['must'].extend(self.type_list[options['type']](keyword, keyword_type=keyword_type))
            if DEBUG:
                # url = "http://mini.eastday.com/nsa/210106201136374480817.html"
                url = "http://ishare.ifeng.com/c/s/81d2P147ns0"
                query_dict = {
                    "bool":{
                        "should":[
                            {
                                "term": {
                                    "url.keyword": {
                                        "value": url
                                    }
                                }
                            },

                            {
                                "term": {
                                    "url": {
                                        "value": url
                                    }
                                }
                            }
                        ]
                    }
                }
            for datas, search_afters in ConnectManager.ES.get_setting('DEFAULT').search_by_page_with_searchafter(
                    options['sindex'],
                    doc=None,
                    fields=ESSpider.FieldListEnum.OLD_FULL_FIELDS.value,
                    query={"query": query_dict, 'search_after': search_after} if search_after else {
                        "query": query_dict},
                    sort_fields=[{'post_time': 'desc'}, {'include_time': 'desc'}],
                    return_sort=True,
                    dynamic_search_after=True
            ):
                for post, next_search_after in zip(datas, search_afters):
                    post['__search_after'] = next_search_after
                    yield post, keyword_type

    # 把type假定成post里的属性传进去，方便后续其他处理使用。不过最后一步一定要把这个type弹出
    def push_type_attr(self, data_and_type):
        data_and_type[0]['__type'] = data_and_type[1]
        return data_and_type[0]

    def pop_type_attr(self, data):
        if '__type' in data:
            del data['__type']
        return data

    # 过滤链接为空的
    def filter_empty_url(self, post):
        logger.info(f'URL:{post.get("url", "NO_URL")}')
        logger.info(f'POST_TIME:{post["post_time"]}')
        if post['url']:
            return post

    # 过滤全局黑名单
    def filter_global_exclude_data(self, post, global_exclude):
        if global_exclude.exists((post['title'] or '') + '　;' + (post['text'] or '')):
            logger.info(f'Post {post["url"]} has global exclude word')
        else:
            return post

    # 过滤标题黑名单
    def filter_title_exclude_data(self, post, title_exclude):
        if title_exclude.exists(post['title'] or ''):
            logger.info(f'Post {post["url"]} has title exclude word')
        else:
            return post

    # 转换站点名
    def trans_sitename_from_post(self, post, need_trans_sitenames):
        if any(sitename in post['site_name'] for sitename in need_trans_sitenames):
            post['site_id'], post['site_name'], post['entry_id'], post['entry_name'], post[
                'domain'] = ZKYSite.get_true_entry_and_site_info_by_url(post['url'], post['site_id'] or 0,
                                                                        post['site_name'] or '', post['entry_id'] or 0,
                                                                        post['entry_name'] or '')
        else:
            post['domain'] = URL(post['url']).host
        return post

    # 过滤type为0但是站点不在允许的站点列表里的数据
    def filter_type_0_post(self, post, allowed_sitenames):
        if post['__type'] == 0 and post['site_name'] not in allowed_sitenames:
            return
        return post

    # 去除文章多余空白符
    def normalize_title_and_text(self,post):
        post['text'] = TextFactory((post['text'] or '').replace(chr(160),' ')).nowmalize_tag().replace_multispace_to_space().now
        post['title'] = TextFactory((post['title'] or '').replace(chr(160),' ')).nowmalize_tag().replace_multispace_to_space().now
        return post

    # 添加国家标签
    def add_country_tag(self, post, country_indexes):
        title_country_keyresults = reverse_keyfilter_result(country_indexes.exec_filter((post['title'] or '')))  # 标题国家关键词匹配
        # post['title'] = add_tag_from_keyfilter_result(post['title'] or '', title_country_keyresults,self.TITLE_COUNTRY_TAG)  # 为关键词打tag
        post['title_country'] = '#'.join(set(item[1] for item in title_country_keyresults))  # 设置国家出现的字段
        # 四个部分，(tag名,tag所包含住的文本,tag所包含的文本的起始和结束偏移,tag里所附加的key-value信息)
        post['title_country_range'] = json.dumps(
            [(self.TITLE_COUNTRY_TAG, matched_str, tag_range, (('keyname', keyname),)) for matched_str, keyname, tag_range in
             title_country_keyresults])
        # text和上面同理
        text_country_keyresults = reverse_keyfilter_result(country_indexes.exec_filter((post['text'] or '')))
        # post['text'] = add_tag_from_keyfilter_result(post['text'] or '', text_country_keyresults,self.TEXT_COUNTRY_TAG)
        post['text_country'] = '#'.join(set(item[1] for item in text_country_keyresults))
        post['text_country_range'] = json.dumps(
            [(self.TEXT_COUNTRY_TAG, matched_str, tag_range, (('keyname', keyname),)) for matched_str, keyname, tag_range in
             text_country_keyresults])
        return post

    # 标识监管机构
    def add_important_field(self, post, important_rules):
        if post['site_name'] in important_rules['j_names'] or important_rules['j_keyfilters'].exec_filter(post['title']):
            post['regulatory'] = True
        else:
            post['regulatory'] = False
        if post['site_name'] in important_rules['c_names']:
            post['central'] = True
        else:
            post['central'] = False
        return post

    # 添加重点资讯分类
    def en_add_important_field(self, post, id_category_map):
        entry_id = post.get('entry_id', 0) or 0
        if entry_id in id_category_map and id_category_map[entry_id]:
            post['category'] = id_category_map[entry_id]
        return post

    # 修改媒体库里的site_name
    def modify_media_name(self, post, media_names_map):
        # TODO 这里跑完新增数据以后，要再把 entry_id 改成 media_id
        media_id = post.get('entry_id', 0) or 0
        if media_id in media_names_map and media_names_map[media_id]:
            post['site_name'] = media_names_map[media_id]
        return post

    def en_modify_media_name(self, post, media_names_map):
        entry_id = post.get('entry_id', 0) or 0
        if entry_id in media_names_map and media_names_map[entry_id]:
            post['site_name'] = media_names_map[entry_id]
        return post

    # 添加title_hash
    def add_title_hash(self, post):
        post['title_hash'] = ''.join(post['title'].casefold().translate(self.no_char_translate).split())
        if not post['title_hash'].isprintable():
            post['title_hash'] = ''.join(c for c in post['title_hash'] if c.isprintable())
        post['title_hash'] = trans_to_md5(post['title_hash'])
        return post

    def en_add_title_hash(self, post):
        post['title_hash'] = ' '.join(post['title'].casefold().translate(self.no_char_translate).split())
        if not post['title_hash'].isprintable():
            post['title_hash'] = ''.join(c for c in post['title_hash'] if c.isprintable())
        post['title_hash'] = trans_to_md5(post['title_hash'])
        #
        # post['title_hash'] = re.sub(r'[^\S\r\n]+', ' ', post['title_hash'])
        # if not post['title_hash'].isprintable():
        #     post['title_hash'] = ''.join(c for c in post['title_hash'] if c.isprintable())
        # post['title_hash'] = trans_to_md5(TextFactory(post['title']))
        return post

    def handle(self, *args, **options):
        global DEBUG
        DEBUG = options['debug']
        # 计算时间，优先last
        if options['last']:
            options["from"] = lastday(options['last'], time_str=None, to_datetime_str=True)
            options["to"] = today(time_str=None, to_datetime_str=True)

        if not options['english']:
            # 获取中文数据源变量
            source_datas, source_others = self.load_rule_data(options)
            self.type_list = self.cn_type_list
            # 过滤文本
            global_exclude_words = ReIndexNode(words=source_others.global_black_list, flags=re.I)
            title_exclude_words = ReIndexNode(words=source_others.title_black_list, flags=re.I)
        else:
            # 英文版获取数据源变量
            source_datas, source_others = self.en_load_rule_data(options)
            self.type_list = self.en_type_list

        # # 如果type为5那么动态生成配置
        # if options['type'] == 5:
        #     source_data = list(more_itertools.windowed(datetime_range(options["from"], options["to"]), 2))
        if options['type'] < 4:
            source_data = list(zip_longest(source_datas[options['type']], (options['type'],), fillvalue=options['type']))
        elif options['type'] == 4:
            source_data = list(
                chain.from_iterable(zip_longest(datas, (i,), fillvalue=i) for i, datas in enumerate(source_datas)))

        # 计算起始下标
        from_index, to_index = self.cacl_from_and_to_index(options, source_data)
        # 获取当前完成状态信息
        data_version, version_args_json = self.get_or_create_data_version(options, from_index=from_index,
                                                                          to_index=to_index)
        # 获取现在配置里的读取的下标
        from_index = version_args_json['from']

        useful_get = lambda dict_data, target, default=None: dict_data.get(target) if dict_data.get(target,default) else default

        country_indexes = ZKYCountry.get_country_indexes() if not options['english'] else ZKYCountry.get_en_country_indexes()  # 国家AC自动机索引

        # 监管关键词
        j_objs = ZKYRegulatoryObjects.objects.all().values_list('name', flat=True)
        j_names = ZKYRegulatoryUrls.objects.all().values_list('name', flat=True)
        c_names = ZKYCentralUrls.objects.all().values_list('name', flat=True)

        j_keyfilters = BaseKeyFilter(j_objs)
        important_rules = {
            'j_names': j_names,
            'j_keyfilters': j_keyfilters,
            'c_names': c_names
        }

        posts_bulk_module = ESBulk(bulk_index=options['index'], bulk_doc=options['doc'],
                                   op_type=ESBulk.BulkModeEnum.IF_EXISTS_UPDATE_IF_NOT_EXISTS_CREATE,
                                   id_func=lambda post: trans_to_md5(post['url']), has_search_after=False,
                                   split_date=True)
        if not options['no_point']:
            point_line_module = ZJPointToESLineModule(has_search_after=False)
            point_line_module.title_md5_key = options['use_title_cache']
            point_line_module.sentence_md5_key = options['use_sentence_cache']
            points_bulk_module = ESBulk(bulk_index=options['point_index'], bulk_doc='zj_doc',
                                        op_type=ESBulk.BulkModeEnum.IF_NOT_EXISTS_CREATE,
                                        id_func=lambda post: trans_to_md5(post['point_text'][:100]),
                                        has_search_after=False, split_date=True)

        # cache缓存到100个就上传
        cache_posts = []
        if not options['no_point']:
            point_cache_posts = []

        # 获取search_after
        search_after = json.loads(data_version.search_after)

        if not options['english']:
            # 定义中文pipline
            pipline = (
                DataPipline()
                    .regist_func_by_data(self.push_type_attr)  # 把type列表和数据绑定在一起，然后把type作为属性__type写入到post里，以供其他不知情函数可以正常处理post。但是最后一步要弹出__type
                    .regist_func_by_data(self.filter_empty_url)  # 过滤链接不存在的
                    .regist_func_by_data(self.filter_title_exclude_data, title_exclude=title_exclude_words)  # 标题过滤
                    .regist_func_by_data(self.filter_global_exclude_data, global_exclude=global_exclude_words)  # 全局屏蔽词过滤
                    .regist_func_by_data(self.trans_sitename_from_post, source_others.trans_sitenames)  # 转换需要转换的站点名
                    .regist_func_by_data(self.modify_media_name, media_names_map=source_others.media_name_map)  # 媒体库的站点名的转换
                    .regist_func_by_data(self.filter_type_0_post,
                                         allowed_sitenames=source_others.author_with_sitenames)  # 按作者上数据时筛选只上对应几个渠道的数据
                    .regist_func_by_data(self.add_zky_include_time) # 添加日期
                    .regist_func_by_data(self.normalize_title_and_text) # 去除多余空格
                    .regist_func_by_data(self.add_country_tag, country_indexes=country_indexes)  # 添加国家标签
                    .regist_func_by_data(self.add_important_field, important_rules=important_rules)  # 重点资讯，添加央媒信息
                    .regist_func_by_data(self.add_title_hash)  # 添加title_hash

                    .regist_func_by_data(self.pop_type_attr)  # 与第一步对应，弹出__type
            )
        else:
            # 定义英文pipline
            pipline = (
                DataPipline()
                    .regist_func_by_data(self.push_type_attr)  # 把type列表和数据绑定在一起，然后把type作为属性__type写入到post里，以供其他不知情函数可以正常处理post。但是最后一步要弹出__type
                    .regist_func_by_data(self.filter_empty_url)  # 过滤链接不存在的
                    .regist_func_by_data(self.normalize_title_and_text)  # 文本标准化
                    .regist_func_by_data(self.add_country_tag, country_indexes=country_indexes)  # 添加国家标签
                    .regist_func_by_data(self.en_modify_media_name, media_names_map=source_others.entry_name_map)  # 媒体库的站点名的转换
                    .regist_func_by_data(self.add_zky_include_time) # 添加日期
                    .regist_func_by_data(self.en_add_important_field, id_category_map=source_others.id_category_map)  # id 和 category 映射，并添加 category 属性
                    .regist_func_by_data(self.en_add_title_hash)  # 添加title_hash
                    .regist_func_by_data(self.pop_type_attr)  # 与第一步对应，弹出__type
            )

        self.no_char_translate = TextFactory.char_translate
        if options['debug']:
            cache_size = 1
        else:
            cache_size = 500
        next_search_after = None
        final_search_after = None
        for post in pipline(self.load_datas(options, locals())):

            # 添加缓存
            cache_posts.append(post)
            final_search_after = post.pop('__search_after')
            # 大于cache_size进行专家观点提取和上ES
            if len(cache_posts) > cache_size:
                logger.info(f'start to process cache,len {len(cache_posts)}')
                if not options['no_point']:
                    for point_data in point_line_module.run(cache_posts):
                        point_cache_posts.extend(point_data)
                    logger.info(f'point cache len,len {len(point_cache_posts)}')
                logger.info(f'will to zky es')
                try:
                    sucess, faild, _ = list(posts_bulk_module.run(cache_posts))[0]
                    logger.info(f'bulk to zky es success:{sucess} faild:{faild}')
                    version_args_json['post_sucess'] += sucess
                    version_args_json['post_faild'] += faild
                    next_search_after = final_search_after
                    data_version.search_after = json.dumps(next_search_after)
                    data_version.args = json.dumps(version_args_json)
                    data_version.save()

                except Exception as e:
                    logger.exception('bulk to zky es error')

                cache_posts.clear()

                if not options['no_point']:
                    logger.info(f'will to point es')
                    # 插入专家观点表
                    try:
                        sucess, faild, _ = list(points_bulk_module.run(point_cache_posts))[0]
                        logger.info(f'bulk to point es success:{sucess} faild:{faild}')
                        version_args_json['point_sucess'] += sucess
                        version_args_json['point_faild'] += faild

                    except Exception as e:
                        logger.exception('bulk to point es error')
                    logger.info('bulk point over')
                    point_cache_posts.clear()
                pass
        else:
            if cache_posts:
                logger.info(f'start to process cache,len {len(cache_posts)}')
                if not options['no_point']:
                    for point_data in point_line_module.run(cache_posts):
                        point_cache_posts.extend(point_data)
                    logger.info(f'point cache len,len {len(point_cache_posts)}')
                logger.info(f'will to zky es')
                try:
                    sucess, faild, _ = list(posts_bulk_module.run(cache_posts))[0]
                    logger.info(f'bulk to zky es success:{sucess} faild:{faild}')
                    version_args_json['post_sucess'] += sucess
                    version_args_json['post_faild'] += faild
                    next_search_after = final_search_after

                except Exception as e:
                    traceback.print_exc()
                    print('bulk to zky es error')
                cache_posts.clear()
                if not options['no_point']:
                    logger.info(f'will to point es')
                    # 插入专家观点表
                    try:
                        sucess, faild, _ = list(points_bulk_module.run(point_cache_posts))[0]
                        logger.info(f'bulk to point es success:{sucess} faild:{faild}')
                        version_args_json['point_sucess'] += sucess
                        version_args_json['point_faild'] += faild

                    except Exception as e:
                        traceback.print_exc()
                        print('bulk to point es error')
                    point_cache_posts.clear()
        data_version.search_after = json.dumps(next_search_after)
        data_version.args = json.dumps(version_args_json)
        data_version.save()

    @staticmethod
    def type_0(obj, *args, **kwargs):
        return [
            {
                "bool": {
                    "should": [
                        {
                            "term": {
                                "author_name": {
                                    "value": obj
                                }
                            }
                        },
                        {
                            "term": {
                                "author_name.keyword": {
                                    "value": obj
                                }
                            }
                        }
                    ]
                }
            }
        ]

    @staticmethod
    def type_1(obj, *args, **kwargs):
        return [
            {
                "bool": {
                    "should": [
                        {
                            "prefix": {
                                "url": {
                                    "value": f'http://{obj}'
                                }
                            }
                        },
                        {
                            "prefix": {
                                "url": {
                                    "value": f'https://{obj}'
                                }
                            }
                        },
                        {
                            "prefix": {
                                "url.keyword": {
                                    "value": f'http://{obj}'
                                }
                            }
                        },
                        {
                            "prefix": {
                                "url.keyword": {
                                    "value": f'https://{obj}'
                                }
                            }
                        }
                    ]
                }
            }
        ]

    @staticmethod
    def type_2(obj, *args, **kwargs):
        return [
            {
                "term": {
                    "media_id": {
                        "value": obj
                    }
                }
            }
        ]

    @staticmethod
    def type_3(obj, *args, **kwargs):
        return [
            {
                "term": {
                    "entry_id": {
                        "value": obj
                    }
                }
            }
        ]

    @staticmethod
    def type_4(obj, *args, **kwargs):
        return getattr(Command, f'type_{kwargs["keyword_type"]}')(obj)



    @staticmethod
    def type_en_0(obj, *args, **kwargs):
        return [
            {
                "bool": {
                    "should": [
                        {
                            "term": {
                                "entry_id": {
                                    "value": obj
                                }
                            }
                        }
                    ]
                }
            }
        ]

    def add_zky_include_time(self, post):
        post['zky_include_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return post
