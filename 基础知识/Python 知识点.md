
#### 代码怎么想的就怎么写，不要怕。  

#### 文档，每天读一点，有个印象，遇到能想起来，到时候再深入学。   


## Python 相关  

#### 多用 ?、help，多用 dir    

```python 
多用问号  
getattr?  
dict.get? 
dict?

help(getattr)
help(dict.get)  
```

### 基础  

for 循环是变量赋值；函数传参也是变量赋值；函数位置实参本质上就是多变量对应位置赋值；所以等号右边的是实参，等号左边的是形参；所以在 Django 的视图函数中进行查询的时候，等号右边是前端传进来的参数，等号左边的是 Django 的字段名；类的实例化中类加括号才是实例化，小写的名字也是变量赋值。  

函数传参传的是引用，本质上都是指向一个东西，这个变了，所有的就都变了。  


### 字符串  

#### f 字符串  

要在字符串中插入变量的值，使用 f 字符串，将要插入的变量放在花括号内。这样，当 Python 显示字符串时，将把每个变量都替换为其值。  

使用 f 字符串可以实现信息个性化显示。  


#### translate() 和 maketrans() 

```python 
In [2]: s = 'abcde'

In [4]: s.maketrans({'c': ''})
Out[4]: {99: ''}

# str.maketrans?  
Return a translation table usable for str.translate().  

In [6]: s.translate(str.maketrans({'c': ''}))
Out[6]: 'abde'

# str.translate?
Replace each character in the string using the given translation table.  

In [7]: s
Out[7]: 'abcde'

In [8]: s.translate(str.maketrans({'c': 'm'}))
Out[8]: 'abmde'
```


#### join() 拼接正则查询条件  

l = ['长征精神', '红军精神', '第二次世界大战', '抗日战争', '第一次世界大战', '二战', '一战', '抗美援朝']

`"(" + ")|(".join(l) + ")"`


#### ord() 和 chr()

ordinals 序列数，就是第几第几  

```python 
In [20]: ord('A')
Out[20]: 65

In [21]: chr(65)
Out[21]: 'A'
```


#### casefold()    

就是更彻底的 lower()  

```python 
In [15]: s = "Abc"

In [16]: s.casefold()
Out[16]: 'abc'
```

#### 字符串和索引拼接  

```python 
In [1]: s = "北国风光"

In [2]: ''.join([f'[{i}]{val}' for i, val in enumerate(s)])
Out[2]: '[0]北[1]国[2]风[3]光'
```
 
#### splitlines 函数  

"""字符串""".splitlines() 把字符串转换成列表   


#### UserString  


#### html.unescape

将字符串 s 中的所有命名和数字字符引用 (例如 `&gt;`, `&#62;`, `&#x3e;`) 转换为相应的 Unicode 字符。  

比如把 `&ldquo;` 转换成左双引号，这要就可以通过 translate() 和 maketrans() 去掉了   



### 列表  

#### 列表取值  

一种是通过索引取值，比如 li[3]，一种是通过 for 循环遍历  


#### 列表推导式  

```python 
In [28]: [x for x in range(7)]
Out[28]: [0, 1, 2, 3, 4, 5, 6]

In [29]: [x for x in range(7) if x > 3]
Out[29]: [4, 5, 6]

# 没有 else 的时候，if 必须要放在 for 循环后面，放在前面会报错  

In [30]: [x ** 2 for x in range(7) if x > 3]
Out[30]: [16, 25, 36]

In [31]: [x ** 2 if x > 3 else x ** 3 for x in range(7)]
Out[31]: [0, 1, 8, 27, 16, 25, 36]

# 有 else 条件的时候，if 和 else 必须要放在 for 循环前面，否则会报错
```

#### 切片  

切片是为了使用处理列表的部分元素  

切片非常有用，用的地方非常多，比如文章分页，比如 batch 取数据、比如训练集验证集的切分  


#### ::切片  

```python 
In [25]: li = list(range(10))

In [26]: li[2:6]
Out[26]: [2, 3, 4, 5]

In [27]: li[2:]
Out[27]: [2, 3, 4, 5, 6, 7, 8, 9]

In [28]: li[2:8:3]
Out[28]: [2, 5]

In [29]: li[2::3]  # 都是 start, stop, end，这里是把 end，省略了，所以有两个冒号，而且必须要有两个冒号，一个冒号就是最普通的切片了。  
Out[29]: [2, 5, 8]
```


#### 列表转字典  

```python 
In [20]: t = ('a', 1), ('b', 2)

In [21]: t
Out[21]: (('a', 1), ('b', 2))

In [22]: list(t)
Out[22]: [('a', 1), ('b', 2)]

In [23]: dict(list(t))
Out[23]: {'a': 1, 'b': 2}
```


#### sort  

sort 原地排序，不返回值，从小到大排序  

```python 
In [1]: l = [1, 9, 4, 6]
In [2]: l.sort()
In [3]: l
Out[3]: [1, 4, 6, 9]
```


### 字典  

#### 字典 pop()  

字典使用 pop 键的时候，如果存在就返回键的值，如果不存在就返回指定的默认值。  

```python 
In [66]: d
Out[66]: {'a': 1, 'b': 2}

In [67]: d.pop('a', 3)
Out[67]: 1

In [68]: d
Out[68]: {'b': 2}

In [69]: d.pop('a', 3)
Out[69]: 3
```


#### 遍历字典  

遍历字典，默认是遍历 key  

```python 
In [53]: d = {'a': 1, 'b': 2}

In [54]: d
Out[54]: {'a': 1, 'b': 2}

In [55]: for key in d:
    ...:     print(key)
    ...: 
a
b
```

进入了这一层了，就可以用 d['a'] 这样的方式通过键取值。  

如果是取每一条，就用形如 d['a'] 这样的方式拿到每一条的值，如果每一条内部还有嵌套，就再用 for 循环去取更深层的值。  

```python 
In [58]: for key, value in d.items():
    ...:     print(key, value)
    ...: 
a 1
b 2

In [59]: for key in d.keys():
    ...:     print(key)
    ...: 
a
b

In [60]: for value in d.values():
    ...:     print(value)
    ...: 
1
2
```


### for 循环  

for 循环的作用就是批量处理数据，对所有的数据执行相同的操作。  

for 循环可以让计算机自动完成大量的重复的工作。  

如果没有 for，如果元素很多，就会包含大量重复的代码，而且如果元素个数发生变化的时候，就必须要修改代码，会非常麻烦。  

for 循环，可以对每个元素执行任何操作。  

for 循环本质上就是通过不断调用 next() 函数实现的。  

```python 
for x in [1, 2, 3, 4, 5]:
    print(x)
```

本质上就是下面这种方式实现的。  

```python 
it = iter([1, 2, 3, 4, 5])
while True:
    try:
        # 获得下一个值:
        x = next(it)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break
```


### if 语句 

if 语句可以让我们在遍历列表的时候，对特定的元素采取特定的措施。  

for 循环以一种方式处理列表中的大多数元素，if 语句以另一种方式处理特定的元素。  


### 迭代器和生成器  

很可能就是一个链表，每次指针移动一个位置。for 循环遍历很可能也是移动指针。  

就是断点。  

如果调用一个有 100 篇文章的列表，就会占用非常大的存储空间，如果我们仅仅需要看前几篇文章，那后面绝大多数元素占用的空间都白白浪费了。  

所以，如果可以不必调用完整的列表，而是可以按需返回，那就可以节省大量的空间。这就是迭代器和生成器被创造出来和被广泛应用的原因。  

这是一种惰性计算（lazy evaluation）。  

有两种使用场景：
1、按需生成。  
2、某个事情执行一部分，另一部分在某个事件发生后再执行下一部分，实现异步。  


#### 生成器  

generator 就是 iterator 的一种，以更优雅的方式实现的 iterator。  

一种是推导式

```python 
In [123]: g = (x ** 2 for x in range(10))

In [124]: type(g)
Out[124]: generator

In [125]: next(g)
Out[125]: 0

In [126]: next(g)
Out[126]: 1

In [127]: next(g)
Out[127]: 4

In [128]: next(g)
Out[128]: 9

# 可以用 for 循环遍历生成器，生成器也是可迭代对象  
In [129]: for i in g:
     ...:     print(i)
     ...: 
16
25
36
49
64
81
```

一种是使用 yield  

```python 
In [112]: def get_one_num():
     ...:     for i in range(10):
     ...:         yield i
     ...: 

In [113]: type(get_one_num)    # 不加括号是函数
Out[113]: function

In [114]: type(get_one_num())    # 加了括号是返回值，就是 yield 
Out[114]: generator

In [115]: gen = get_one_num()

In [116]: next(gen)
Out[116]: 0

In [117]: next(gen)
Out[117]: 1

In [118]: next(gen)
Out[118]: 2
```


### 函数  

不写重复代码的好处，一个是节省写的工作量，直接用就行了，不用每次调用都重新写；一个是修改的时候只改一个地方就好了。  

不加括号的时候是函数，加括号以后就是返回值。  

```python 
In [132]: def my_fun():
     ...:     return 1
     ...: 

In [133]: type(my_fun)
Out[133]: function

In [134]: type(my_fun())
Out[134]: int
```


#### lambda 函数  

lambda 返回一个函数，和 def f(x) 是一样的。  

def 是用来处理大的任务的，lambda 是为了实现简单函数而设计的，用的时候简单清晰，不用再写一个函数，直接嵌套在代码段中就行。  

简洁清晰，使用方便。  

```python 
In [29]: def f(x):
    ...:     return x ** 2
    ...: 

In [30]: f(3)
Out[30]: 9

In [31]: f1 = lambda x: x ** 2

In [32]: f1(3)
Out[32]: 9

# 冒号后面是 return 的值，lambda 后面的是参数。  

In [33]: f2 = lambda x, y: x + y

In [34]: f2(3, 4)
Out[34]: 7
```


#### 参数  

位置实参赋值本质上就是变量的对应位置赋值。  

关键字参数就是分别赋值，所以位置无关紧要。  

\*args 和 \*\*kwargs 很可能也都是变量赋值用的。  


### 类  

不加括号是类，加了括号就是返回值，就是实例  

```python 
In [40]: type(list)
Out[40]: type

In [41]: type(list())
Out[41]: list
```

### 其他  

#### \n \t  

\n 可能是 new line  
\t tab 制表符  


#### yield  

多用 yield  




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


### 内置函数  

#### exec 函数  

这个函数支持动态执行 Python 代码。 object 必须是字符串或者代码对象。  

```python 
In [26]: exec('print("Hello world")')
Hello world
```


#### eval 函数

```python
In [24]: x = 1

In [25]: eval('x+1')
Out[25]: 2
```


#### filter 类

filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true.

```python 
n [72]: list(filter(abs, [-1, 0, 1]))
Out[72]: [-1, 1]
```


#### map 类  

map(func, \*iterables) --> map object

Make an iterator that computes the function using arguments from
each of the iterables.

```python 
In [14]: list(map(abs, [-2, -1, 0, 2, 5]))
Out[14]: [2, 1, 0, 2, 5]

In [15]: def my_square(x):
    ...:     return x ** 2

In [16]: list(map(my_square, [-2, -1, 0, 2, 5]))
Out[16]: [4, 1, 0, 4, 25]
```

#### next 函数 

next(iterator[, default])

Return the next item from the iterator. If default is given and the iterator
is exhausted, it is returned instead of raising StopIteration.


#### Path 函数  

Path 拼接是 / 'program' / 'result.txt' 这样的形式  

pandas 的 read_excel() 读取的类型是字符串，Path 的结果是一个 Path 对象，所以路径要变成字符串，方法就是 str(Path 对象)，或 Path 对象.\_\_str__()  

可以用 open(路径字符串, 'w', encodig='utf-8') 写入文件，也可以在 path 对象后面跟 .open('w', encoding='utf-8') 写入文件  


#### reduce 函数  

```python 
from functools import reduce 

l = [1, 2, 3, 4, 5] 
reduce(lambda x, y: x + y, l)

先 1 + 2，再 3 + 3，再 6 + 4 等等  
```

#### partial 函数  

partial(函数，参数)，partial 函数，把参数绑定到函数上。  


### collections 包

#### defaultdict 类  

解决一键多值的问题  

```python 
In [1]: from collections import defaultdict

In [2]: d = defaultdict(list)

In [3]: d['a'].append(1)
In [4]: d['a'].append(2)
In [5]: d['a'].append(3)

In [6]: d
Out[6]: defaultdict(list, {'a': [1, 2, 3]})

In [7]: d['b'].append(4)
In [8]: d['b'].append(5)

In [9]: d
Out[9]: defaultdict(list, {'a': [1, 2, 3], 'b': [4, 5]})
```

也可以是集合  

```python 
In [13]: d = defaultdict(set)

In [14]: d['a'].add(1)
In [15]: d['a'].add(2)

In [16]: d
Out[16]: defaultdict(set, {'a': {1, 2}})

In [17]: d['b'].add(3)
In [18]: d['b'].add(4)

In [19]: d
Out[19]: defaultdict(set, {'a': {1, 2}, 'b': {3, 4}})

```

也可以使用字典自带的 setdefault 实现  

```python 
In [20]: d = {}

In [21]: d.setdefault('a', []).append(1)

In [22]: d
Out[22]: {'a': [1]}

In [23]: d.setdefault('a', []).append(2)

In [24]: d
Out[24]: {'a': [1, 2]}

In [25]: d.setdefault('b', []).append(3)

In [26]: d
Out[26]: {'a': [1, 2], 'b': [3]}
```

#### OrderedDict 类  

对字典进行迭代的时候，OrderedDict 会严格按照元素初始添加的顺序进行。  

```python 
n [34]: d = OrderedDict()

In [35]: d['foo'] = 1

In [36]: d['bar'] = 2

In [37]: d['spam'] = 3

In [38]: d['grok'] = 4

In [39]: for key in d:
    ...:     print(key, d[key])
    ...: 
foo 1
bar 2
spam 3
grok 4

In [40]: d
Out[40]: OrderedDict([('foo', 1), ('bar', 2), ('spam', 3), ('grok', 4)])

In [41]: import json

In [42]: json.dumps(d)
Out[42]: '{"foo": 1, "bar": 2, "spam": 3, "grok": 4}'
```

### typing 包

#### Union 

联合类型；Union[X, Y] 的意思是，非 X 即 Y。  


```python 
```

### 非 Python  

#### NaN  

NaN(Not a Number)  


#### 哈希  

哈希算法也叫散列算法, 不过英文单词都是 Hash, 简单一句话概括, 就是可以把任意长度的输入信息通过算法变换成固定长度的输出信息, 输出信息也就是哈希值。  

```python 
In [30]: import hashlib

In [31]: hashlib.md5('你好'.encode(encoding='UTF-8')).hexdigest()
Out[31]: '7eca689f0d3389d9dea66ae112e5cfd7'

In [32]: hashlib.md5('123'.encode(encoding='UTF-8')).hexdigest()
Out[32]: '202cb962ac59075b964b07152d234b70'
```

自己实现的对类进行去重  

```python 
In [65]: hash('hello')
Out[65]: 7769867404179893035

In [66]: class Cat:
    ...:     def __init__(self, name, age):
    ...:         self.name = name
    ...:         self.age = age
    ...:     def __hash__(self):
    ...:         return hash((self.name, self.age))
    ...:     def __eq__(self, other):
    ...:         return self.name == other
    ...: 

In [67]: hash(('hello', 3))
Out[67]: -999010963045695219

In [68]: cat2 = Cat('xiaohua', 3)

In [69]: cat1 = Cat('xiaohua', 3)

In [70]: cat3 = Cat('xiaohu', 3)

In [71]: set([cat1, cat2, cat3])
Out[71]: {<__main__.Cat at 0x7f7803899a10>, <__main__.Cat at 0x7f7811d81e10>}

```


#### 格式转换  

Python 对象是不可以跨平台的，所以和前端交互要变成通用格式，比如 json 字符串或二进制流格式。  

Python 的格式，只有 Python 会解释  

```python
d = {'a': 1}  

json.loads('{"a": 1}')
Out[2]: {'a': 1}    # json.loads() 把 str 转化为 Python 对象  

json.dumps(d)
Out[1]: '{"a": 1}'    # json.dumps() 把 Python 的格式转化成 str  
```


#### and 和 or  

or 遇到第一个为真的就返回，如果都为假就返回最后一个  

or 第一个为真就取第一个，第一个为假就取第二个。取优先级高的。    
`1 or 0` 取 1，`0 or 1` 取 1  

如果两个都是假，取第二个  
`0 or False` 取 False   


and 第一个为真就取第二个，第一个为假就取第一个  
`1 and 6` 取 6  



#### 功能去重  

```python 
char_translate = str.maketrans({i: '' for i in
                                        r"""!"#$%｜&'()*+,-./:;<=>?@[\]^_`{|}~“”？，！～＠＃％＾＊【】（）、。：；’／
                                        ＼＿－＝☆★○●◎◇◆□€■△▲※→←↑↓¤♂♀〖〗『』」「‖〃‘……￥·"""})
removed_duplicates_result = set()  
for text in result:
    title = text[0].translate(char_translate)
    if title not in removed_duplicates_result:
        removed_duplicates_result.add(title)
    else:
        continue
```

#### 展示去重  

去除标题里的标签：`text0 = re.sub(r'(<.*?>)|(\n)', '', text[0])`  



### Python 基础知识点  

不可变类型，赋值就是复制。  

range() 就是 range 类型 `type(range(1, 3))`  

魔法方法。Python 解释器会在不同的场景下自动调用不同的魔法方法。比如 [] 调用 \_\_getitem__()，print() 调用 \_\_str__()，== 调用 \_\_eq__()，in 调用 \_\_contains__()  

```python 
setattr(self, 'k', 10) 完全等价于 self.k = 10  
```

自省。hasattr()，不管你是不是，只要有这个，就当你是。这就是“鸭子类型”。  

next() 用于获得第一个对象。  

生成器，取元素的时候，一次只取一个，取完一个以后程序不再执行，调一次给一次。  

yield 迭代器，返回一个生成器，一次返回一个，调一次给一次。  

list() 取的时候，会一次取完，因为 list 所做的事情就是，取到所有的元素，把这些元素组成一个 list 列表。  

自己再走一遍装饰器流程。   


#### 内置函数  

读文档，查内置函数。  

all() 里所有元素都为真，就返回真。  

any() 任意一个为真，就返回真。  

UserString 查。  

frozenset()  

locals 返回局部上下文。  

globals 返回文件上下文。  

可以在实例方法里打印  
```python 
print(locals())
print(globals())
```


#### 函数  

在大函数里，所有的地方都可以使用大函数的变量，这就是函数作用域。  

global 的作用就是使用更外层的上下文。  

内层作用域无法修改外层变量，这是 Python 里写死的规则。  

nonlocal 的作用就是在内层操作外层变量，就像是在外层操作外层变量完全等效，就相当于，把内层函数 def inner(): 这一行去掉，inner 函数的内容左移一个 tab 完全等效。  

周一：
周二：江南小碗菜  
周三：大同刀削面  
周四：  
周五：  
周六：
周日：爆肚粉、田老师  


#### 类 

type 创建类，所有的类都是 type 的实例。  

```python 
In[2]: class A:
  ...:     pass 
  ...: 

In[3]: type(A)
Out[3]: type

In[4]: isinstance(A, type)
Out[4]: True
```

类是一种模板，改模板，所有的就都变了。  

对象可能是抽象层面的东西。  

对象是一种模板。  

```python 
a = A()  
```

实例是类执行完 \_\_new__() 方法以后创建的对象。  

先 \_\_new__() 再 \_\_init__()  

self 就是 a，self 和 A 完全是两个东西。  

self 是形参，a 是实参，self 是对 a 的引用  

a 是类 A() 执行完 \_\_new__() 方法以后创建的对象。  

创建完实例以后，这个实例就可以拥有一些自己的东西。  

实例拥有类变量，实例拥有实例变量，类不拥有实例变量。  

内部优先级更高，这样就可以实现定制。  

对变量本身修改才是修改变量，append() 不修改变量，append() 改的是变量内部的元素。就好比是在桶里增加或减少了东西，但是桶本身并没有变化，桶还是这个桶，所以变量没有变。列表和字典都是这样。  

比如：  
```python 
class A:
    m = []

    def __init__(self):
        self.__class__.m.append(1)
```

所以在 \_\_init__() 中，给 self 增加设置属性，并不会改变 self。和 append() 是一样的。  

\_\_new__() 的时候创建了一个实例，这个实例就是实例 a，就是 self。  

所以 \_\_init__() 的第一个参数就是 self。  

所以 \_\_init__() 一直都是在对 a 进行各种操作。这种操作就是定制。所以不写 \_\_init__() 也没有关系，代表 a 和 A 是一样的。  

Python 函数，是最常见的拥有作用域的东西。作用域是 C 语言中最常见的概念。Python 中弱化了这种概念。Python 中 if 没有作用域，while 也没有作用域。  

函数就是一个黑盒，函数与外界进行信息传递只有三种方式，参数、返回值和上下文。  

input -> 黑盒操作 -> output  

参数就是输入，返回值就是输出。上下文就是外部可见的东西。  

上下文例子？上下文要再好好看一看。  

把实参赋值给形参，就是变量赋值。  

信息是属于函数的，另一个函数可以接收上一个函数的返回值，也就是上一个函数的输出，这样另一个函数就拿到了上一个函数的信息。  

数据都是在函数里的，函数是有作用域的，那么类里的数据是怎么传递的？  

在类里，实例方法的参数都有一个 self 参数，这个 self 就是传递信息用的，可以贯穿所有的处理方法之中。  

self 的作用是可以使得实例能够访问类中的属性和方法。  

而且方法在处理 self 的时候，并不会改变 self 的地址，实例方法做的就是给 self 增加减少或修改属性。  

```python 
a = A()  
a.f()  

# 等效于
A.f(a)
```
点前面是谁，就尝试传谁。  

A.f() 报错，尝试传值失败了，就不传了。这也说明了类 A 和 self 也就是实例 a，完全就是两个东西。  

```python 
@classmethod  
def fc(cls):
    pass 
```

classmethod 是类层面的方法，就是对类的定制，而不是对实例的定制了，所以就和 self 没关系了。  

```python 
class A:
    m = [1, 2]

    @classmethod
    def fc(cls):
        print(cls.m)
```

fc() 经过装饰器，成为类方法以后，还是可以通过 a.fc() 调用，原因是实例可以获取到类里的全部信息。  

调用 `a.fc()` 实际上是在调用 `A.fc(a.__class__)`  

类方法和实例方法都是自动传参，也就是点前面是谁，就是尝试传谁。  

@staticmethod 不会自动传参，而是要手动传参，@staticmethod 会使点功能失效。  

静态方法不做依赖于类和实例的操作，而是做一些通用的无关的操作，静态方法传的是和自己这个类和实例都无关的参数，静态方法可以有返回值，静态方法的功能就是信息传递。  

需要传参数，就用类方法和实例方法。  

cls 就是 A()，self 就是 a  

\_\_init__() 之后，所有的方法都可以使用包含初始化属性的这个 self。  

如果在普通的实例方法中写了 `self.m = 12`，而且调用了这个方法，那么这个方法之后的所有的实例方法都可以使用这个属性。  

```python 
def __init__(self):
    self.m = 12 
    
def f(self):
    self.m = 12  
```

\_\_init__() 方法和 f() 方法是完全一样的，都是实例方法。在这一点上没有任何差别。\_\_init__() 中实现的功能，在其他的实例方法里完全都可以实现。  

两个下划线的作用就是为了避免和普通方法在命名上产生冲突。  

唯一的差别就是，在实例化的时候，也就是在执行 a = A() 的时候，\_\_init__() 方法在最开始的时候会执行一次，而且是必定会执行的。  

名字可以任意取，不是一定要叫 self，这就是个变量名。  

a.f() 就是 A.f(a)，在类中，实例方法是 def f(self)，这个就是把 a 传给了 self，就是 self = a，赋值。所以这本质上就是变量赋值，所以可以取任意的名字，比如取名叫做，self111  

```python 
class A:
    def f(self111):
        self111.k = 12
        print(self111.k)
        return self111

a = A()  
a.f()  
```



链式调用，返回 self，self 就是传递信息用的。比如 a.f().f1() 就是先执行 A.f(a)，得到结果，返回 self，也就是 a，所以就成了 a.f1()，也就实现了链式调用。而且 f1() 函数还拿到了 f() 函数的信息。   

property 装饰器，和 property() 是完全等效的。作用就是把一个方法变成可以像属性一样调用。外面调用的时候，看起来就想是个属性。主要是用于复杂的取值赋值操作，这样更符合操作习惯，而且有很好的可扩展性，外部完全不用改。  


super().\_\_init__(make, model, year)  

就是调用父类的初始化方法，使得子类拥有父类初始化方法中的属性，说白了就是把父类中的初始化方法中的代码复制到了子类的初始化方法中，如果不写 super，子类的初始化方法中没有父类定义的这些属性，因为子类方法会覆盖父类的同名方法。  




