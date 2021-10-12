"""
    一个数据线性处理流模块
"""
import itertools
from functools import partial

class NO_DATA:...

class DataPipline:
    def __init__(self):
        self.register_funcs = [] # 注册的函数们（目前暂未保留函数签名）
        self.limit_count = -1

    def __call__(self,datas,limit=-1):
        """
            返回经过全部处理流程后的数据生成器
            可以通过指定limit来确定返回最多多少数据，如果为-1的话返回全部数据
        """
        self.limit_count=limit
        if self.limit_count>=0:
            self.register_funcs.append(self.limit_func)
        return self.make_register_funcs_to_func(datas)

    def limit_func(self,datas):
        for _,data in itertools.takewhile(lambda x:x[0]<self.limit_count,enumerate(datas)):
            yield data


    def make_register_funcs_to_func(self,datas):
        """
            返回将全部函数整合后的最终函数
        """
        _func = datas
        for func in self.register_funcs:
            _func=func(_func)
        return _func


    def wrap_by_field(self,datas,func,field_name,*args,default=None,**kwargs):
        """
            对字段处理函数进行包装成该类需要的函数
        """
        for data in datas:
            data[field_name] = func(data.get(field_name, default),*args,**kwargs)
            yield data
    def wrap_by_fields_return_func(self,func,fields_name,*args,default=None,defaults=None,out_field=NO_DATA,out_fields=NO_DATA,yield_to_list=False,**kwargs):
        """
            装饰多值输入的函数，使其模拟从数据里取多个字段进行处理然后返回的函数
        """
        defaults = defaults or (default for _ in range(len(fields_name)))
        def _itemgetter(_data):
            for _field_name,_default in zip(fields_name,defaults):
                yield _data.get(_field_name,_default)
        def _itemgetter_list(_data):
            return [_data.get(_field_name,_default) for _field_name,_default in zip(fields_name,defaults)]

        __itemgetter = _itemgetter_list if yield_to_list else _itemgetter

        def wrap_by_fields__inner_out(datas):
            for data in datas:
                data[out_field] = func(__itemgetter(data), *args, **kwargs)
                return data
        def wrap_by_fields__inner_outs(datas):
            for data in datas:
                for field, result in zip(out_fields, func(__itemgetter(data), *args, **kwargs)):
                    data[field] = result
                yield data
        def wrap_by_fields__inner_in(datas):
            for data in datas:
                for field, result in zip(fields_name, func(__itemgetter(data), *args, **kwargs)):
                    data[field] = result
                yield data
        if out_field==NO_DATA and out_fields==NO_DATA:
            return wrap_by_fields__inner_in
        elif out_field==NO_DATA:
            return wrap_by_fields__inner_outs
        else:
            return wrap_by_fields__inner_out


    def regist_func_by_data(self,func,*args,**kwargs):
        """
            注册处理一整条数据的函数
        """
        def regist_func_by_data__inner(datas):
            for data in datas:
                result = func(data,*args,**kwargs)
                if result is not None:
                    yield result
        self.register_funcs.append(regist_func_by_data__inner)
        return self
    def regist_func_by_datas(self,func,*args,**kwargs):
        """
            注册遍历处理全部数据的函数
        """
        self.register_funcs.append(partial(func,*args,**kwargs))
        return self

    def regist_func_by_field(self,func,field_or_fields_name,*args,default=None,defaults=None,out_field=NO_DATA,out_fields=NO_DATA,yield_to_list=False,**kwargs):
        """
            注册处理数据中的字段的函数
        :param func: 函数名
        :param field_or_fields_name: 字段或字段列表，如果是字段列表，那必须是list类型
        :param args: 函数的其余args参数
        :param default: 如果输入的数据的字段数据只有一条字段，那么这个就是那个字段的默认值
        :param defaults: 如果输入的数据字段数据是多个字段，那么就是多个字段的的默认值。如果输入是多个字段，那么默认值为default字段*字段列表的长度
        :param out_field: 输出结果到的字段名
        :param out_fields: 输出结果到的字段列表名
        :param yield_to_list: 如果是多字段输入的话，那么字段值列表组成的数据是不是列表类型，False的话是生成器类型
        :param kwargs: 函数的其余kwargs参数
        :return:
        """
        if isinstance(field_or_fields_name,list):
            self.register_funcs.append(self.wrap_by_fields_return_func(func,field_or_fields_name,*args,default=default,defaults=defaults,out_field=out_field,out_fields=out_fields,yield_to_list=yield_to_list,**kwargs))
        else:
            self.register_funcs.append(partial(self.wrap_by_field,func=func,*args,field_name=field_or_fields_name,default=default,**kwargs))
        return self

    pass





