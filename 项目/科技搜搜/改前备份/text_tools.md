
```python 
import html
import re
from collections import deque
from functools import wraps
from itertools import chain
from operator import itemgetter
from queue import Queue
from typing import Union, Dict

from bidict import bidict


def reverse_keyfilter_result(result_dict: dict):
    """
        把形如
        {
            "中国大陆":[("清华大学",(24,28)),("中科院",(13,16))],
            "台湾":[("台北",(18,20))]
        }
        的数据排序成
        [('中科院', '中国大陆', (13, 16)), ('台北', '台湾', (18, 20)), ('清华大学', '中国大陆', (24, 28))]
    :param result_dict:
    :return:
    """

    def keyfilter_yield_result():
        for name, true_name_and_range_list in result_dict.items():
            for true_name_and_range in true_name_and_range_list:
                yield (true_name_and_range[0], name, true_name_and_range[1])

    def yield_sorted_result():
        last = None
        for now in sorted(keyfilter_yield_result(), key=itemgetter(2)):
            if (not last) or last[2][-1] < now[2][-1]:
                yield now
                last=now

    return list(yield_sorted_result())


class TextFactory(str):
    char_translate = str.maketrans({i: '' for i in
                                    r"""!"#$%｜丨&'()*《》+＋,-—./:;<=>?@[\]^_`{|}~“．”？，！～＠＃％＾＊【】（）、。：；’／＼＿
                                    －＝☆★○●◎◇◆□€■△▲※→←↑↓¤♂♀〖〗『』」「‖〃‘……￥·"""})
    stop_cpl = re.compile(r"[\?\!;。？！；\r\n]")
    stop_reverse_cpl = re.compile(r"(?:.*?[\?\!;。？！；\r\n])+")
    stop_char = '?!。？！\r\n'
    en_stop_cpl = re.compile(r"[\?\!;\.？！；\r\n]")
    en_stop_reverse_cpl = re.compile(r"(?:.*?[\?\!;\.？！；\r\n])+")
    en_stop_char = '?!.？！\r\n'

    def __new__(cls, value, *args, **kwargs):
        return str.__new__(cls, value)

    def __init__(self, value):
        double_char_str = '“”‘’《》【】{}《》（）()〝〞＜＞﹝﹞<>«»‹›〔〕〈〉［］「」｛｝〖〗『』""''``'
        self.char_map = bidict({double_char_str[i]: double_char_str[i + 1] for i in range(0, len(double_char_str), 2)})
        self.__target_str = value
        self.__source_str = value
        self.__last_str = value

    def log_last(func):
        """
            通过loa_last参数监控是否要记录此函数处理之前的结果，默认不记录
        :param func:
        :return:
        """

        @wraps(func)
        def warp(self, *args, log_last=False, **kwargs) -> "TextFactory":
            result = func(self, *args, **kwargs)
            if log_last:
                self.__last_str = self.__target_str
            self.__target_str = result or ''
            return self

        return warp

    @log_last
    def replace_all_not_word_char_to_null(self) -> "TextFactory":
        return ''.join(self.casefold().translate(self.char_translate).split())

    @log_last
    def add_tag_from_words_and_tags_result(self, words: list, tags: list) -> "TextFactory":
        _s = ''.join(f'<{t}>{w}</{t}>' for w, t in zip(words, tags))
        if not _s.isprintable():
            return ''.join(c for c in _s if c.isprintable())
        return _s

    @log_last
    def add_tag_from_ranges_and_tags_result(self, ranges: list, tags: list) -> "TextFactory":
        return ''.join(f'<{t}>{self.now[r[0]:r[1]]}</{t}>' for r, t in zip(ranges, tags))

    @log_last
    def add_tag_from_lac(self, lac) -> "TextFactory":
        return ''.join(f'<{t}>{w}</{t}>' for w, t in zip(*lac.run(self.now)))

    @log_last
    def get_from_xmltag_with_tags(self, xmltags: list = [re.compile(r'<PER></PER>')], start=0, end=-1, group_id=0):
        """
            取第一个符合匹配的
            倒序匹配的话一定(.*?(正则内容))+，然后用.group 2 取
        :param xmltags:
        :return:
        """
        now_count = 0
        if end == -1:
            end = len(self.now)
        if not isinstance(xmltags, (tuple, list)):
            xmltags = (xmltags,)
        for xmltag_re_cpl in xmltags:
            search_result = xmltag_re_cpl.search(self.now, start, end)
            if search_result and search_result.group(group_id):
                return search_result.group(group_id)

    @log_last
    def add_tag_from_keyfilter_result(self, keyfilter_result: list, tag_name: str,
                                      sentense_before_offset=0) -> "TextFactory":
        """
            根据列表化后的结果为文本加上标签
            eg:
                input:
                    text:               '讨论一下中国和霍普斯金大学的关系'
                    keyfilter_result:   [('中国', '中国大陆', (4, 6)), ('霍普斯金大学', '美国', (7, 13))]
                    tag_name:           'titlecountry'
                output:
                    '讨论一下<titlecountry keyname="中国大陆">中国</titlecountry>和<titlecountry keyname="美国">霍普斯金大学</titlecountry>的关系'
        :param keyfilter_result: 转换成列表后的keyfilter的结果
        :param tag_name: 标签名
        :return: 字符串
        """
        text = self.now
        text_list = []
        start_index = 0
        for tag_item in keyfilter_result:
            text_list.extend((
                text[start_index:tag_item[2][0] - sentense_before_offset],  # 前缀
                f'<{tag_name} keyname="{tag_item[1]}">',  # tag标签，keyname是主关键字，比如说中国大陆
                tag_item[0],  # 真正匹配的关键词
                f'</{tag_name}>'
            ))
            start_index = tag_item[2][1] - sentense_before_offset
        else:
            text_list.append(text[start_index:])
        return ''.join(text_list)

    @log_last
    def replace_multispace_to_space(self, repl=' ') -> "TextFactory":
        """
            去除多余空格
        :param repl: 被替换东西
        :return:
        """
        return re.sub(r'[\r\n]+', '\n', re.sub(r'[^\S\r\n]+', ' ', self.now))

    @log_last
    def replace_tag_to_others(self, repl='') -> "TextFactory":
        return re.sub(r'<[/a-zA-Z]+?.*?>', repl, self.now)

    @log_last
    def replace_countrytag_to_others(self, tag_name, source_extra_data='', repl='', repl_tag='',
                                     extra_data='') -> "TextFactory":
        """
            替换指定tag为指定字符串，如果repl_tag不为None或空字符串，那么只替换tag名并且添加extra_data内容
        :param tag_name:
        :param repl:
        :param repl_tag:
        :return:
        """

        def sub_repl_rule(matched):
            if matched.group(1)[-1] != '/':
                return f'{matched.group(1)}{repl_tag} {extra_data}>'
            else:
                return f'{matched.group(1)}{repl_tag}>'

        def source_extra_data_repl(matched):
            if repl_tag:
                return f'<{repl_tag} {extra_data} {matched.group(len(matched.groups()))}{repl_tag}>'
            else:
                return f'{repl}{matched.group(len(matched.groups()))[1:-2]}{repl}'

        if source_extra_data:
            return re.sub(r'(<)' + tag_name + r'\s*' + source_extra_data + r'[^/]*?(>[^<>]*</)' + tag_name + '>',
                          source_extra_data_repl, self.now) if repl_tag else re.sub(
                r'<' + tag_name + r'\s*' + source_extra_data + r'[^/]*?>', repl, self.now)
        else:
            return re.sub(r'(</?)' + tag_name + r'[^/]*?(>)', sub_repl_rule, self.now) if repl_tag else re.sub(
                r'</?' + tag_name + r'[^/]*?>', repl, self.now)




    @log_last
    def chunk_tag_with_max_size(self, tag_name, _max_size=120, search_flag_str=None) -> "TextFactory":
        """
            根据最大长度自动和要保留的高亮标签字段来自动截取合适的文本
        :param tag_name:
        :param _max_size:
        :param search_flag_str:
        :return:
        """
        start_offset = self.now.find(search_flag_str or f'<{tag_name}') - 1
        prefix = '……'
        endfix = '……'
        str_max_len = len(self.now)
        temp_last_tag_offset = self.now.find(f'</{tag_name}>', start_offset)
        first_offset, last_offset = start_offset, temp_last_tag_offset + 3 + len(tag_name)
        max_size = _max_size + (
                (last_offset - start_offset) - (temp_last_tag_offset - self.now.find('>', start_offset) - 1))
        if start_offset == 0:
            prefix = ''
        # 创建标点符号表
        flag_offset_list = []
        for c in self.now[first_offset::-1]:
            first_offset -= 1
            if first_offset <= 0:
                flag_offset_list.insert(0, -1)
                break
            if c in ['。', '！', '~', '？', '\r', '\n']:
                flag_offset_list.insert(0, first_offset + 1)
                break
            elif c in [',', '…', ';', '.', '，']:
                flag_offset_list.insert(0, first_offset + 1)
        keywords_index = len(flag_offset_list)  # 在此下标之后都是后缀，这是分界线

        for c in self.now[last_offset:]:
            if c in ['。', '！', '~', '？', '\r', '\n']:
                flag_offset_list.append(last_offset)
                break
            elif c in [',', '…', ';', '.', '，']:
                flag_offset_list.append(last_offset)
            elif last_offset == str_max_len - 1:
                flag_offset_list.append(str_max_len)
            last_offset += 1
        flag_start_offset, flag_end_offset = 0, len(flag_offset_list) - 1
        mode = 0  # 0，一昧的缩减后方，1,一昧的缩减前方，2，同时缩减
        while flag_start_offset < keywords_index and flag_end_offset >= keywords_index:
            if flag_offset_list[flag_end_offset] - flag_offset_list[flag_start_offset] <= max_size:
                break
            if mode == 0:
                if flag_end_offset > keywords_index:
                    flag_end_offset -= 1
                else:
                    mode = 1
                    flag_end_offset = len(flag_offset_list) - 1
            elif mode == 1:
                if flag_start_offset < keywords_index - 1:
                    flag_start_offset += 1
                else:
                    mode = 2
                    flag_start_offset = 1
                    flag_end_offset = len(flag_offset_list) - 2
                    is_first_add = True
            else:
                if is_first_add and flag_start_offset < keywords_index - 1:
                    flag_start_offset += 1
                    is_first_add = False
                elif flag_end_offset > keywords_index:
                    flag_end_offset -= 1
                    is_first_add = True
                else:
                    # 这种是最极限的左右都没标点还超过最大长度
                    return self.now[start_offset - max_size // 2:start_offset + max_size // 2]
            pass
        if flag_offset_list[flag_start_offset] == 0:
            prefix = ''
        if flag_offset_list[flag_end_offset] in [str_max_len - 1, str_max_len]:
            endfix = ''
        return f'{prefix}{self.now[flag_offset_list[flag_start_offset] + 1:flag_offset_list[flag_end_offset]]}{endfix}'

    @log_last
    def nowmalize_tag(self, extra_re_list: list = []) -> "TextFactory":
        re_list = [
            (r'<br[\s/]*>', '\n'),
            (r'<.+?>', ''),
        ]
        for re_str, repl in chain(extra_re_list, re_list):
            self.__target_str = re.sub(re_str, repl, self.now)
        return self.__target_str

    def return_last(self):
        self.__target_str = self.__last_str
        return self

    def find_true_char(self, s: str, start_offset: int, is_front_search=True,last_level=None,lan='chs'):
        """
            从s字符串的start_offset开始查找，is_front_search决定是往前还是往后找，找到停止符停止句子切分
            逻辑基本思路为：
                停止操作不能无脑按停止符停止，因而必须要有上下文
                这里的上下文是指成对的标点符号所组成的作用域上下文
                    比如说“开始读书《钢铁是怎样炼成的》这本书。然而他说过？”这句话
                    如果是从“钢铁是怎样炼成的”里的“怎”开始往前后或往后搜索的话，那么最大的搜索范围一定在最邻近的作用域中，也就是撑死在“《钢铁是怎样炼成的》”里
                    同理如果是从“这本书”里的“本”开始搜索的话，那么最大的范围在整个话里，但是特殊的又不能断在更里层的作用域里，比如说这里的书名号里
                这里我们定义一个队列充当栈用，里面存储这种成对的符号，初始队列为空
                当往前找的时候我们允许进入成对符号的右符号，此时就是就是右符号入栈，但是不能停在里面，所以一定至少要等这个右符号对应的左符号让它弹出才有可能停止
                我们将栈的元素数定义为level的话，那么就是level为0时才能进行停止操作
                反之如果是往右寻找的话，那么就都是相反的了，允许左符号入栈，对应的右符号发现时出栈
        :param flag:
        :param count:
        :param s: 要遍历的字符串
        :param start_offset: 开始查找的地方
        :param is_front_search: 是否往前查找，False是往后查找
        :return: 返回指定方向的第一个断句的下标
        """
        # 空字符串直接返回
        stop_char = (self.stop_char if lan=='chs' else self.en_stop_char)
        if not s:
            return 0,0,0
        if is_front_search:
            step = -1
            limit_offset = -1
            two_char_map = self.char_map.inverse
            start_offset = min(max(start_offset,-1),len(s)-1) # start_offset可以为-1，代表在0前，但是不能更往前了
            # 当前字符是否是停止符，因为start_offset可能小于0，所以此时无效
            if start_offset>=0 and s[start_offset] in stop_char:
                start_offset = max(0, start_offset - 1)
        else:
            step = 1
            limit_offset = len(s)
            # 没找到时从0开始查
            if start_offset<0:
                start_offset = 0
            two_char_map = self.char_map

        level_deque = deque()
        negative_level = 0
        for c_i in range(start_offset, limit_offset, step):
            c = s[c_i]
            if level_deque.__len__() > 0 and c == two_char_map[level_deque[-1]]:
                negative_level -= 1
                level_deque.pop()
            elif c in two_char_map.keys():
                negative_level+=1
                level_deque.append(c)
            elif level_deque.__len__() == 0 and c in two_char_map.values():
                if c not in stop_char and (last_level is None or last_level!=negative_level):
                    negative_level -= 1
                    continue
                negative_level -= 1
                return c_i - step, negative_level,1

            elif level_deque.__len__() == 0 and c in stop_char and (last_level is None or last_level==negative_level):
                return c_i - step, negative_level,2
        else:
            return limit_offset - step, negative_level,3


    @log_last
    def chunk_tag_with_max_size_v2(self, tag_name=None, search_flag_str=None,search_index=None,lan='chs') -> str:
        """
            根据要保留的高亮标签字段来自动截取合适的文本
        :param tag_name:
        :param search_flag_str:
        :return:
        """
        self.now = html.unescape(self.now)
        if not self.now:
            return self.now
        start_offset = search_index if search_index is not None else self.now.find(search_flag_str or f'<{tag_name}')
        s = self.now
        prefix = '……'
        endfix = '……'
        end, end_level,end_flag = self.find_true_char(s, start_offset, is_front_search=False,lan=lan)
        start,start_level,start_flag = self.find_true_char(s, start_offset-1, last_level=end_level,lan=lan)
        end+=2
        str_max_len = len(s)

        # if start_flag == end_flag:
        #     return f'{prefix}{s[start:end]}{endfix}'

        if start <= 0:
            prefix = ''
        if end >= str_max_len-1:
            endfix = ''
        if s[start:end][-1] in ['\r', '\n']:
            return f'{prefix}{s[start:end]}{endfix}'
        return f'{prefix}{s[start:end]}{endfix}'

        # 创建标点符号表


        # prefix = '……'
        # endfix = '……'
        # str_max_len = len(self.now)
        # temp_last_tag_offset = self.now.find(f'</{tag_name}>', start_offset)
        # first_offset, last_offset = start_offset, temp_last_tag_offset + 3 + len(tag_name)
        # # max_size = _max_size + ((last_offset - start_offset) - (temp_last_tag_offset - self.now.find('>', start_offset) - 1))
        # if start_offset == 0:
        #     prefix = ''
        # # 创建标点符号表
        #
        # start_offset = self.stop_reverse_cpl.search(self.now, 0, start_offset)
        # if start_offset is None:
        #     start_offset = 0
        # else:
        #     start_offset = start_offset.end()
        # end_offset = self.stop_cpl.search(self.now, last_offset)
        # if end_offset is None:
        #     end_offset = str_max_len
        #     true_str = self.now[start_offset:end_offset] + '。'
        # else:
        #     end_offset = end_offset.end()
        #     true_str = self.now[start_offset:end_offset]
        #     if true_str[-1] in ['\r', '\n']:
        #         true_str += '。'
        #
        # if start_offset in [0, 1]:
        #     prefix = ''
        # if end_offset in [str_max_len]:
        #     endfix = ''
        # return f'{prefix}{true_str}{endfix}'

    @property
    def last(self):
        return self.__last_str

    @property
    def source(self):
        return self.__source_str

    @property
    def now(self):
        return self.__target_str

    @now.setter
    def now(self, value):
        self.__target_str = value

    def __str__(self):
        return self.__target_str

    # 让str自带的方法生效，不过str自带的方法只能最后调用
    def __getattribute__(self, item):
        if hasattr(str, item):
            return str.__getattribute__(self.__target_str, item)
        else:
            return str.__getattribute__(self, item)


def add_tag_from_keyfilter_result(text: str, keyfilter_result: list, tag_name: str) -> str:
    """
        根据列表化后的结果为文本加上标签
        eg:
            input:
                text:               '讨论一下中国和霍普斯金大学的关系'
                keyfilter_result:   [('中国', '中国大陆', (4, 6)), ('霍普斯金大学', '美国', (7, 13))]
                tag_name:           'titlecountry'
            output:
                '讨论一下<titlecountry keyname="中国大陆">中国</titlecountry>和<titlecountry keyname="美国">霍普斯金大学</titlecountry>的关系'
    :param text: keyfilter_result所计算的文本
    :param keyfilter_result: 转换成列表后的keyfilter的结果
    :param tag_name: 标签名
    :return: 字符串
    """
    text_list = []
    start_index = 0
    for tag_item in keyfilter_result:
        text_list.extend((
            text[start_index:tag_item[2][0]],  # 前缀
            f'<{tag_name} keyname="{tag_item[1]}">',  # tag标签，keyname是主关键字，比如说中国大陆
            tag_item[0],  # 真正匹配的关键词
            f'</{tag_name}>'
        ))
        start_index = tag_item[2][1]
    else:
        text_list.append(text[start_index:])
    return ''.join(text_list)

class NO_MATCHED_TAG_VALUE:...
def split_html_attrs(attrs_str:str)->Dict:
    if not attrs_str.strip():
        return {}
    str_flag=None
    k_or_v_list=['','']
    k_or_v_index=0
    _tmp_locals={}
    k_v_str_list=[]
    for i,c in enumerate(attrs_str):
        # k或v前面有空格  or 连续空格的第二个及之后的  过滤
        if c.isspace() and (k_or_v_list[k_or_v_index]=='' or (i==0 or attrs_str[i-1].isspace())):
            continue
        # k或非字符串的v的结束
        if str_flag is None and k_or_v_list[k_or_v_index]!='' and (c=='=' or c.isspace()):
            if k_or_v_index==1:
                k_v_str_list.append('='.join(k_or_v_list))
                k_or_v_list = ['', '']
                str_flag = None
            k_or_v_index^=1
        # 字符串v的结束
        elif k_or_v_index==1 and str_flag is not None and str_flag==c and (not (i>2 and attrs_str[i-1]=='\\' and not (i>3 and attrs_str[i-2]=='\\'))):
            k_or_v_list[k_or_v_index] += c
            k_v_str_list.append('='.join(k_or_v_list))
            k_or_v_list = ['', '']
            str_flag = None
            k_or_v_index=0
        elif k_or_v_index==1 and str_flag is None and (c=='"' or c=="'"):
            k_or_v_list[k_or_v_index] += c
            str_flag = c
        else:
            k_or_v_list[k_or_v_index] += c
    else:
        if k_or_v_list[1]!='':
            k_v_str_list.append('='.join(k_or_v_list))
    exec(';'.join(k_v_str_list),{},_tmp_locals)
    return _tmp_locals
def to_html_attrs_str(attrs_dict:Dict)->str:
    return ' '.join('{}={}'.format(k,'"'+v.replace('"','\\"')+'"' if isinstance(v,str) else v) for k,v in (attrs_dict.items() if isinstance(attrs_dict,(dict))  else attrs_dict))



def replace_tag(text:str,text_flag_range:list,tag_name=None, tag_attr_kwargs:Union[str,Dict]={}, repl='', repl_tag='',extra_data:Union[str,Dict]={},replace_count=-1):
    """
        把tag标识好的文本替换相关tag文本或者替换tag里的内容
    :param text:原文本，不带标签
    :param text_flag_range: xml标签列表，格式为[(xml标签名,tag所包含住的文本,tag所包含的文本的起始和结束偏移(二元元组),tag里所附加的key-value信息(列表，里面是二元元组做元素，分别代表k和v)) ]
    :param tag_name: 要查找以替换的标签名
    :param tag_attr_kwargs: 要查找的标签名的附加k,v参数，可以是 “a=1 b='233hello'”这种形式，也可以是字典
    :param repl:要把整个xml包含起来的部分替换的结果
    :param repl_tag:要把tag_name替换成什么
    :param extra_data:要在替换后的tag里加什么额外的k,v元素，和tag_attr_kwargs一样可以是字典也可以是字符串
    :param replace_count:最多替换几次
    :return: 替换后的字符串
    >>> s = '0123456789'
    >>> text_range = [('text_country','01',(0,2),(('keyword','中国'),)),('text_country','46',(4,7),(('keyword','美利坚'),)),('text_country','8',(8,9),(('keyword','中国'),))]
    >>> replace_tag(s,text_range,repl_tag='my_tag',tag_name='text_country',replace_count=1)
    '<my_tag>01</my_tag>23456789'
    >>> replace_tag(s,text_range,repl_tag='my_tag',tag_name='text_country')
    '<my_tag>01</my_tag>23<my_tag>46</my_tag>7<my_tag>8</my_tag>9'
    >>> replace_tag(s,text_range,repl_tag='my_tag',tag_name='title_country')
    '0123456789'
    >>> replace_tag(s,text_range,repl_tag='my_tag',tag_name='text_country',tag_attr_kwargs='keyword="中国"')
    '<my_tag>01</my_tag>234567<my_tag>8</my_tag>9'
    >>> replace_tag(s,text_range,repl_tag='my_tag',tag_name='text_country',tag_attr_kwargs={"keyword":"中国"})
    '<my_tag>01</my_tag>234567<my_tag>8</my_tag>9'
    >>> replace_tag(s,text_range,repl='啊啊',tag_name='text_country',tag_attr_kwargs={"keyword":"中国"})
    '啊啊234567啊啊9'
    """
    now_count=0
    replace_text_list = []
    text_start_offset = 0

    if isinstance(tag_attr_kwargs,str):
        tag_attr_kwargs = split_html_attrs(tag_attr_kwargs)
    if isinstance(extra_data,str):
        extra_data = split_html_attrs(extra_data)
    extra_data_str = to_html_attrs_str(extra_data)
    if extra_data_str:
        extra_data_str=' '+extra_data_str
    for _tag_name,_matched_str,(_start_offset,_end_offset),_attr_tuples in text_flag_range:
        if len(_attr_tuples)>0 and not isinstance(_attr_tuples[0],(tuple,list)):
            _attr_tuples = (_attr_tuples,)
        _attr_dict = dict(_attr_tuples)
        # 略过不匹配的标签
        if tag_name is not None and (_tag_name!=tag_name or not all(_attr_dict.get(search_k,NO_MATCHED_TAG_VALUE)==search_v for search_k,search_v in tag_attr_kwargs.items())):
            continue
        # 达到替换次数上限
        if replace_count!=-1 and now_count>=replace_count:
            break
        # 加入替换后的文本
        if repl:
            replace_text_list.extend(
                (
                    text[text_start_offset:_start_offset],
                    repl,
                )
            )
        else:
            replace_text_list.extend(
                (
                    text[text_start_offset:_start_offset],
                    f'<{repl_tag}{extra_data_str}>',
                    text[_start_offset:_end_offset],
                    f'</{repl_tag}>'
                )
            )
        now_count+=1
        text_start_offset=_end_offset
    replace_text_list.append(text[text_start_offset:])
    return ''.join(replace_text_list)

def add_tag(text:str,text_flag_range:list):
    text_list = []
    text_start_offset = 0
    for _tag_name, _matched_str, (_start_offset, _end_offset), _attr_tuples in text_flag_range:
        if len(_attr_tuples)>0 and not isinstance(_attr_tuples[0],(tuple,list)):
            _attr_tuples = (_attr_tuples,)
        keyword_str = to_html_attrs_str(_attr_tuples)
        keyword_str = keyword_str and ' '+keyword_str
        text_list.extend((
            text[text_start_offset:_start_offset],
            f'<{_tag_name}{keyword_str}>',
            text[_start_offset:_end_offset],
            f'</{_tag_name}>'
        ))
        text_start_offset = _end_offset
    text_list.append(text[text_start_offset:])
    return ''.join(text_list)
```
