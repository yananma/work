
#### 代码怎么想的就怎么写，不要怕。  

#### 文档，每天读一点，有个印象，遇到能想起来，到时候再深入学。   

`dir(dict)`  


### Python 相关  


#### Path 函数  

Path 拼接是 / 'program' / 'result.txt' 这样的形式  

pandas 的 read_excel() 读取的类型是字符串，Path 的结果是一个 Path 对象，所以路径要变成字符串，方法就是 str(Path 对象)，或 Path 对象.\_\_str__()  

可以用 open(路径字符串, 'w', encodig='utf-8') 写入文件，也可以在 path 对象后面跟 .open('w', encoding='utf-8') 写入文件  


#### splitlines 函数  

"""字符串""".splitlines() 把字符串转换成列表   


#### reduce 函数  

```python 
from functools import reduce 

l = [1, 2, 3, 4, 5] 
reduce(lambda x, y: x + y, l)

先 1 + 2，再 3 + 3，再 6 + 4 等等  
```

#### partial 函数  

partial(函数，参数)，partial 函数，把参数绑定到函数上。  


#### 时间相关  

时间相关的，多用 datetime。少用 time，time ，没什么方法，

```python 
In [1]: from datetime import datetime

In [2]: datetime.now()
Out[2]: datetime.datetime(2021, 8, 8, 18, 33, 2, 50696)

In [3]: d.strftime("%Y-%m-%d %H:%M:%S")
Out[3]: '2021-08-08 18:34:09'

```

datetime 可以通过 . 看都有什么方法，比如 year、month、day、hour、minute、second 等等  


#### 装饰器  

`__call__` 方法在可调用对象加括号的时候调用。  

实例加括号会调用类的 `__call__` 方法，类加括号会调用元类的 `__call__` 方法。  


```python
from functools import wraps

def arg_dec(ts=None):
    s = ts
    print(f'arg_dec:{s}')
    def outer(func):
        print(f'outer:{s}')
        @wraps(func)
        def inner(*args,**kwargs):
            print(f'inner:{s}')
            print(f'inner:{args}\t{kwargs}')
            return func(*args,**kwargs)
        print(f'inner finish:{s}')
        return inner
    print(f'outer finish:{s}')
    return outer


@arg_dec(45)
def add(a,b):
    return a+b
```


```python 
```

### 非 Python  

#### 格式转换  

Python 对象是不可以跨平台的，所以和前端交互要变成通用格式，比如 json 字符串或二进制流格式。  

Python 的格式，只有 Python 会解释  

```python
d = {'a': 1}  

json.dumps(d)
Out[1]: '{"a": 1}'    # json.dumps() 把 Python 的格式转化成 str  

# dumps 方法返回的是 JSONEncoder.encode(obj)
# JSONEncoder.encode() 方法做的事情就是 Return a JSON string representation of a Python data structure. 
# encode() 方法所做的事情非常简单 就是 return ''.join(chunks)  

json.loads('{"a": 1}')
Out[2]: {'a': 1}    # json.loads() 把 str 转化为 Python 对象  

# loads 方法 Deserialize a JSON document to a Python object.  
```


#### JSON  

Json 内部必须是双引号  
'{"a": 1}' 这种是正确的  
"{'a': 1}" 这种是错误的  

存数据库的时候用  


#### and 和 or  

or 第一个为真就取第一个，第一个为假就取第二个。取优先级高的。    
`1 or 0` 取 1，`0 or 1` 取 1  
如果两个都是假，取第二个  
`0 or False` 取 False   

如果有多个条件遇到第一个为真的就返回  


and 第一个为真就取第二个，第一个为假就取第一个  
`1 and 6` 取 6  


