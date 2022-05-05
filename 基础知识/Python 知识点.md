
# Python 文档就是最好的笔记，多读文档     


## Python 相关  

#### 多用 . 然后结合 ?、help，多用 dir    

```python 
多用问号  
getattr?  
dict.get? 
dict?

help(getattr)
help(dict.get)  
```

### 基础  

for 循环是变量赋值；函数传参也是变量赋值；函数位置实参本质上就是多变量对应位置赋值；\*args args 是元组名，所以起什么名字都不重要，\* 才是核心，\* 往里拆一层，把整个的拆成独立的；所以等号右边的是实参，等号左边的是形参；所以在 Django 的视图函数中进行查询的时候，等号右边是前端传进来的参数，等号左边的是 Django 的字段名；类的实例化中类加括号才是实例化，小写的名字也是变量赋值。  

函数传参传的是引用，本质上都是指向一个东西，这个变了，所有的就都变了。  


### 字符串  


#### 命名  

好的命名是实现易读性的关键。   

变量命名：   
返回值统一叫做 result   
从 ES 取出的一批数据叫做 batch_data    
前缀：prefix   
后缀：suffix   


函数命名   
去重叫 dedupe    
上一个 prev，下一个 next    



#### f 字符串  

所有的路径拼接都用 f 字符串实现。   

要在字符串中插入变量的值，使用 f 字符串，将要插入的变量放在花括号内。这样，当 Python 显示字符串时，将把每个变量都替换为其值。  

使用 f 字符串可以实现信息个性化显示。  


#### [replace](https://docs.python.org/zh-cn/3/library/stdtypes.html#str.replace)  

strip() 只能去掉前后的字符，可以用 replace 来实现内部 strip 功能   

```python 
s = s.replace("-", "")  
```


#### format  

```python 
print("Hello, {0}".format(username.title())) 
```


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

`print('\\" OR \\"'.join(li))`  

`print('"' + '", "'.join(li) + '"')` 把 splitlines 的结果转换成 1 行  

`print('["' + '", "'.join(li) + '"]')` 列表  


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


#### center()  

```python 
In [4]: s = 'hello'

In [5]: s.center(20)
Out[5]: '       hello        '

In [6]: s.center(10)
Out[6]: '  hello   '

In [7]: s.center(7)
Out[7]: ' hello '

In [8]: s.center(6)
Out[8]: 'hello '

In [9]: s.center(5)
Out[9]: 'hello'

In [10]: s.center(3)
Out[10]: 'hello'
```

#### find()  

str.find(sub[, start[, end]])  
返回子字符串 sub 在 s[start:end] 切片内被找到的最小索引。 可选参数 start 与 end 可以理解为切片。 如果 sub 未被找到则返回 -1。  

sub 是子字符串。  

```python 
In [2]: s = 'hello world'

In [3]: s
Out[3]: 'hello world'

In [4]: type(s)
Out[4]: str

In [5]: s.find('l')
Out[5]: 2

In [6]: s.find('l', 2)
Out[6]: 2

In [7]: s.find('l', 3)
Out[7]: 3

In [8]: s.find('l', 4)
Out[8]: 9
```


#### isspace()  

如果字符串中只有空白字符且至少有一个字符则返回 True ，否则返回 False 。  

```python 
In [2]: s1 = ' hello world  '

In [3]: s1.isspace()
Out[3]: False

In [4]: s2 = ' '

In [5]: s2.isspace()
Out[5]: True

In [6]: s3 = '\t\n'

In [7]: s3.isspace()
Out[7]: True
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


### 数字  

#### Python 给数字前固定位数加零  

[Python给数字前固定位数加零](https://www.cnblogs.com/cymwill/p/6500831.html)

如果是字符串格式  
```python 
n = "123"
s = n.zfill(5)
assert s == "00123"
```

#### 格式化  

```python 
print(f'CNN的测试准确率为{result[1] * 100:.2f}%')
```

如果是数字格式，就用格式化方法  
```python 
In [13]: "%04d" % 50
Out[13]: '0050'

In [14]: "%04d.0" % 50
Out[14]: '0050.0'

In [15]: "%04d.0"% 1234
Out[15]: '1234.0'
```


### 列表  

#### append 和 extend  

```python
# append 
In [1]: nums = [1, 2, 3]

In [2]: new_nums = [4, 5]

In [3]: nums.append(new_nums)

In [4]: nums
Out[4]: [1, 2, 3, [4, 5]]

# extend 
In [5]: nums = [1, 2, 3]

In [6]: new_nums = [4, 5]

In [7]: nums.extend(new_nums)

In [8]: nums
Out[8]: [1, 2, 3, 4, 5]
```


```python 
In [20]: li
Out[20]: 
['北京证券交易所',
 '2022冬奥会,2022年冬奥会,冬残奥会',
 '碳中和,碳达峰',
 '无人驾驶',
 '三胎',
 '双11',
 '双12',
 '房产税',
 '股转系统',
 'bilibili,哔哩哔哩',
 '直播卖货',
 '通胀',
 'iPhone 13',
 '新冠特效药',
 '独董',
 '智能电动车',
 '碳金融',
 'Robotaxi']


In [22]: for item in li:
    ...:     if len(item) == 1:
    ...:         data_list.append(item)
    ...:     else:
    ...:         data_list.extend(item.split(","))
```


#### 计算文本相似度  

```python 
import difflib 

difflib.SequenceMatcher(None, last_word, sentence).quick_ratio() > 0.8
```


#### 列表取值  

一种是通过索引取值，比如 li[3]，一种是通过 for 循环遍历  


#### 列表推导式  

**看到 for 循环就要想一想能不能用列表推导式写**

列表推导式异常强大。如果你的代码里并不经常使用它们，那么很可能你错过了许多写出可读性更好且更高效的代码的机会。  

遇到三行，空列表、for 循环和 append，就肯定可以用列表推导式，再有一个 if 判断，也可以用列表推导式。  

列表推导式的作用只有一个：生成列表。  

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

# 两层 for 循环，前面的那个 for 循环在外层  
In [4]: num_list = [1, 2, 3]

In [5]: char_list = ['a', 'b', 'c']

In [6]: [(num, char) for num in num_list for char in char_list]
Out[6]: 
[(1, 'a'),
 (1, 'b'),
 (1, 'c'),
 (2, 'a'),
 (2, 'b'),
 (2, 'c'),
 (3, 'a'),
 (3, 'b'),
 (3, 'c')]

In [8]: for num in num_list:
   ...:     for char in char_list:
   ...:         print((num, char))
   ...: 
(1, 'a')
(1, 'b')
(1, 'c')
(2, 'a')
(2, 'b')
(2, 'c')
(3, 'a')
(3, 'b')
(3, 'c')

In [9]: [(num, char) for char in char_list for num in num_list]
Out[9]: 
[(1, 'a'),
 (2, 'a'),
 (3, 'a'),
 (1, 'b'),
 (2, 'b'),
 (3, 'b'),
 (1, 'c'),
 (2, 'c'),
 (3, 'c')]
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

In [1]: li = [3, 5, 2, 6]

In [2]: sort_li = li.sort()

In [3]: sort_li

In [4]: sort_li

In [5]: print(sort_li)
None

In [6]: li
Out[6]: [2, 3, 5, 6]
```


#### 对列表中的字段排序  

格式为 [{}, {}, {}]，要按字典的某一个值进行排序   

```python 
img_list = sorted(img_list, key=lambda item: item['image_name'])   
```


### 字典  

模块的命名空间，实例的属性和函数的关键字参数后面都是字典。  

同键名的字典，后面的值会覆盖前面的值。  

```python 
In [1]: d = {'a': 1, 'b': 2, 'a': 3}

In [2]: d
Out[2]: {'a': 3, 'b': 2}
```

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

#### fromkeys()  

创建同 key 字典  

```python 
In [37]: d = {'a': 1, 'b': 2}

In [40]: d1 = {}

In [41]: d1.fromkeys(d)
Out[41]: {'a': None, 'b': None}
```

#### 字典按值排序  

降序排列  

`(ocr_dict.items(), key=lambda d:d[1], reverse=True)`  


### 集合  

遇到 not in 就要想到能不能用集合。     

集合可以去重是因为哈希，同样的内容会存在同一个地方，这样就实现了去重。  

字典的键，不能有重复也是因为哈希。  

判断两个国家列表中不一样的元素，可以用集合的逻辑运算符。  


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

#### 迭代器  

```python
In [8]: s = 'hello'

In [9]: it = iter(s)

In [10]: next(it)
Out[10]: 'h'

In [11]: next(it)
Out[11]: 'e'

In [12]: list(it)
Out[12]: ['l', 'l', 'o']

In [13]: list(it)
Out[13]: []

In [14]: next(it)
---------------------------------------------------------------------------
StopIteration                             Traceback (most recent call last)
<ipython-input-14-bc1ab118995a> in <module>
----> 1 next(it)

StopIteration: 
```


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

**现代程序设计语言中的绝大部分功能，都在程序的函数（Function、Method）中实现。关于函数，最重要的原则是：只做一件事，并且要做好。**

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

lambda 就是对输入做了一次加工（其实所有的函数都是这样）  

lambda 返回一个函数，和 def f(x) 是一样的。  

def 是用来处理大的任务的，lambda 是为了实现简单函数而设计的，用的时候简单清晰，不用再写一个函数，直接嵌套在代码段中就行。  

简洁清晰，使用方便。  

```python 
In [29]: def f(x):
    ...:     return x ** 2
    ...: 

In [30]: f(3)
Out[30]: 9

In [31]: f1 = lambda x: x ** 2    # 这一句是核心，以后看到 lambda 就要想到这一句

In [32]: f1(3)
Out[32]: 9

# 冒号后面是 return 的值，lambda 后面的是参数。  

In [33]: add = lambda x, y: x + y

In [34]: add(3, 4)
Out[34]: 7
```

lambda 里可以写 print  

```python 
In [47]: f = lambda x: print(x)

In [48]: f(3)
3

In [49]: f("hello world")
hello world
```

lambda 里可以写 if   

```python 
In [50]: f = lambda x: print("偶数") if x % 2 == 0 else print("基数")

In [51]: f(5)
基数

In [52]: f(6)
偶数
```

lambda 里可以写列表推导式  

```python 
In [55]: f = lambda x: [item ** 2 for item in x]

In [56]: f([1, 2, 3])
Out[56]: [1, 4, 9]
```


#### 参数  

位置实参赋值本质上就是变量的对应位置赋值。  

关键字参数就是分别赋值，所以位置无关紧要。  

\* 拆元组，\*\* 拆字典    

\*args args 是元组，\*args 是元组中的元素。  

\* 可以把一个可迭代对象拆开作为函数的参数。  

args 是 (1, 2, 3, 4)，\*args 去掉了外层的括号，结果是 1, 2, 3, 4  

```python 
In [19]: def foo(*args):
    ...:     print(f'args: {args}')
    ...: 

In [20]: foo(1, 2, 3, 4)
args: (1, 2, 3, 4)
```

```python 
In [1]: t = (20, 8)

In [2]: *t    # 要放到容器中
  File "<ipython-input-2-f9912a2ca07d>", line 4
SyntaxError: can't use starred expression here


In [3]: list(t)
Out[3]: [20, 8]

In [4]: list(*t)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-0ffad33cd1a4> in <module>
----> 1 list(*t)

TypeError: list expected at most 1 arguments, got 2

In [5]: divmod(20, 8)
Out[5]: (2, 4)

In [6]: t = (20, 8)

In [7]: divmod(t)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-7-f5de22b0f3a4> in <module>
----> 1 divmod(t)

TypeError: divmod expected 2 arguments, got 1

In [8]: divmod(*t)    # t 是 (20, 8) 是一个元组，是一个元素。*t 是 20， 8 是元组里面的元素，在这里是两个元素，可以是多个元素  
Out[8]: (2, 4)
```


\*\*kwargs   

d 是字典，\*\*d 是去掉了最外层的字段括号  

```python 
In [406]: d
Out[406]: {'a': 1, 'b': 2}

In [407]: def foo(**kwargs):
     ...:     print(kwargs)
     ...: 

In [408]: foo(**d)
{'a': 1, 'b': 2}

In [409]: foo(a=1, b=2)
{'a': 1, 'b': 2}
```




### 类  

不加括号是类，加了括号就是返回值，就是实例  

```python 
In [40]: type(list)
Out[40]: type

In [41]: type(list())
Out[41]: list
```

### 其他  

#### 编码  

`# -*- coding:utf-8 -*-`   


#### \n \t  

\n 是 newline  
\t tab 制表符  


#### yield  

多用 yield  




#### 时间相关  

时间相关的，多用 datetime，少用 time。  

```python 
# 把字符串转换成 datetime 对象   
>>> datetime.datetime.fromisoformat('2022-03-31')
datetime.datetime(2022, 3, 31, 0, 0)

# 先安装 dateutil，命令是 pip install python-dateutil  
from dateutil.relativedelta import relativedelta  

>>> current_month = datetime.datetime.now()
>>> current_month
datetime.datetime(2022, 3, 21, 17, 20, 6, 843261)

>>> current_month += relativedelta(months=-1)
>>> current_month
datetime.datetime(2022, 2, 21, 17, 20, 6, 843261)

>>> datetime.datetime.fromisoformat('2022-03-31')
datetime.datetime(2022, 3, 31, 0, 0)

>>> end = datetime.datetime.fromisoformat('2022-03-31')
>>> end += relativedelta(months=-1)
>>> end
datetime.datetime(2022, 2, 28, 0, 0)
```


```python 
In [1]: from datetime import datetime

In [2]: datetime.now()
Out[2]: datetime.datetime(2021, 9, 9, 17, 15, 22, 178434)    # 这里是输出  

In [3]: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
Out[3]: '2021-09-09 17:16:14'

In [4]: s = '2020-01'

In [5]: datetime.strptime(s, '%Y-%m')
Out[5]: datetime.datetime(2020, 1, 1, 0, 0)

In [6]: datetime.strptime(s, '%Y-%m').strftime('%Y年%m月')
Out[6]: '2020年01月'
```

```python
In [59]: import datetime

In [60]: datetime.datetime.now()
Out[60]: datetime.datetime(2021, 9, 15, 17, 52, 54, 6808)

In [61]: datetime.datetime.now() - datetime.timedelta(days=365)
Out[61]: datetime.datetime(2020, 9, 15, 17, 52, 59, 671453)
```

datetime 可以通过 . 看都有什么方法，比如 year、month、day、hour、minute、second 等等  

```python 
In [1]: from datetime import date

In [2]: now = date.today()

In [3]: now
Out[3]: datetime.date(2021, 11, 7)

In [4]: nian = date(2022, 2, 1)

In [5]: nian
Out[5]: datetime.date(2022, 2, 1)

In [6]: days = nian - now

In [8]: days
Out[8]: datetime.timedelta(days=86)

In [9]: days.days
Out[9]: 86
```

删除一天内的数据    

```python 
word_time = datetime.datetime.strptime(key, "%Y:%m:%d %H:%M:%S")
if (datetime.datetime.now() - word_time).days == 0:
    RedisConnect.cache.delete(delete_word_md5)
```

统计运行时间：  
```python 
import time 

start = time.time()    
logger.info('%.2f sec' % (time.time() - start))
```


#### 装饰器  

`__call__` 方法在可调用对象加括号的时候调用。  

实例加括号会调用类的 `__call__` 方法，类加括号会调用元类的 `__call__` 方法。  


```python
In [2]: import time

In [3]: def exec_time(func):
   ...:     def wrapper(*args, **kwargs):
   ...:         start = time.time()
   ...:         res = func(*args, **kwargs)
   ...:         print(f"exec time is {time.time() - start} s")
   ...:         return res
   ...:     return wrapper
   ...: 

In [4]: @exec_time
   ...: def foo():
   ...:     time.sleep(0.5)
   ...: 

In [5]: foo()
exec time is 0.5005528926849365 s
```


#### 协程  

```python 
def grep():
    while True:
        lines = (yield) 
        for line in lines:
            print(line) 
        
        
search = grep() 
next(search) 
search.send([1, 2, 3, 4, 5, 6])  
search.send(["a", "b", "c", "d"])  
```


### 内置函数  

#### repr 函数  

```python 
In [5]: s = 'hello world\n'

In [6]: print(s)
hello world


In [7]: repr(s)
Out[7]: "'hello world\\n'"

In [8]: print(repr(s))
'hello world\n'
```


#### all 函数  

所有的都是 True，结果才是 True  

```python 
In [15]: all(1)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-15-4c9044af74f3> in <module>
----> 1 all(1)

TypeError: 'int' object is not iterable

In [16]: all([1])
Out[16]: True

In [17]: all([1], [])
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-17-84117c3b7519> in <module>
----> 1 all([1], [])

TypeError: all() takes exactly one argument (2 given)

In [18]: all([0, 1, 2])
Out[18]: False

In [19]: all([1, 2])
Out[19]: True
```

字符串 '0' 是 True，数字 0 是 False   

```js  
In [26]: rec_result = ['1', '0', '1', '0', '1']

In [27]: all(rec_result)
Out[27]: True

In [28]: all(map(int, rec_result))
Out[28]: False
```

all([]) 为 True   

```python 
In [1]: all([])
Out[1]: True
```


#### any 函数  

any(iterable)，要存可迭代对象  

错误用法：  

```python 
[any(rec.ocr_modify_if, rec.flower_subtitles_modify_if) for rec in rec_result]    
```

正确用法：   

```python 
[any([rec.ocr_modify_if, rec.flower_subtitles_modify_if]) for rec in rec_result]    
```


有一个为 True 就是 True  

```python 
In [9]: any(1)
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-9-a63f73efd75c> in <module>
----> 1 any(1)

TypeError: 'int' object is not iterable

In [10]: any([])
Out[10]: False

In [11]: any([1])
Out[11]: True

In [12]: any([1], [])
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-12-d956e6390cb8> in <module>
----> 1 any([1], [])

TypeError: any() takes exactly one argument (2 given)

In [13]: any([0, 1, 2])
Out[13]: True

In [14]: any([0, False])
Out[14]: False

In [366]: any([0, True])
Out[366]: True
```

使用案例  

```python 
result_dict = {}
if any(filter(lambda x: x['label']=='1', group)):
    result_dict['label'] = '1' 
else:
    result_dict['label'] = '0' 
```


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

```python 
In [1]: str_list = '[1, 2, 3, 4, 5]'

In [2]: type(str_list)
Out[2]: str

In [3]: eval(str_list)
Out[3]: [1, 2, 3, 4, 5]

In [4]: type(eval(str_list))
Out[4]: list
``` 


#### filter 类

返回 function(item) 为真的那些元素。  

filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true.

```python 
In [72]: list(filter(abs, [-1, 0, 1]))
Out[72]: [-1, 1]

In [10]: list(filter(lambda x: x, [True, False, None, 1, 0]))
Out[10]: [True, 1]
```

filter 必须要传一个函数，所以才有了下面这种写法  

```python 
In [1]: s = '1,0,2,3'

In [2]: s.split(',')
Out[2]: ['1', '0', '2', '3']

In [3]: filter(s.split(','))
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-3-088f38a34497> in <module>
----> 1 filter(s.split(','))

TypeError: filter expected 2 arguments, got 1

In [4]: filter(lambda x: x, s.split(','))
Out[4]: <filter at 0x7f7ca0c418d0>

In [5]: list(filter(lambda x: x, s.split(',')))
Out[5]: ['1', '0', '2', '3']    # 这里 0 没有被筛掉，是因为 0 是字符串  

In [6]: sorted(filter(lambda x: x, s.split(',')))
Out[6]: ['0', '1', '2', '3']

In [8]: list(filter(lambda x: int(x), s.split(',')))
Out[8]: ['1', '2', '3']
```

过滤空数据，过滤的是空字符串    

```python 
li = list(filter(lambda x: x, li))  
```

过滤空格  

```python 
li = list(filter(lambda x: x.strip(), li))  
```

过滤空行  

```python 
list(filter(lambda x: x.strip(), label_list))
```


#### globals 和 locals 函数  

在模块层级上，globals 和 locals 是同一个字段。`set(globals()) - set(locals())` 是空 set()。  

locals 就是这个函数作用域的变量，如果是内层就只是内层，不包含外层，而且是在调用 locals() 之前的变量，如果是外层，只是外层，不包含内层的变量。  

```python 
In [18]: def f3():
    ...:     c = 4
    ...:     print(f'f3 函数的 locals：{locals()}')
    ...:     def f4():
    ...:         d = 5
    ...:         print(f'f4 函数的 locals：{locals()}')
    ...:     return f4()
    ...: 

In [19]: f3()
f3 函数的 locals：{'c': 4}
f4 函数的 locals：{'d': 5}
```

```python 
In [26]: def f5():
    ...:     f = 8
    ...:     print(locals())
    ...:     g = 9
    ...:     print(locals())
    ...: 

In [27]: f5()
{'f': 8}
{'f': 8, 'g': 9}
```

globals 都差不多，就是因为内层的调用晚，所以多一个 e 变量，这个变量只是前后调用的影响造成的差别，并不是内外层造成的差别。  
```python 
In [20]: def f3():
    ...:     d = 4
    ...:     print(f'f3 函数的 locals：{locals()}')
    ...:     print(f'f3 函数的 globals：{globals()}')
    ...:     def f4():
    ...:         e = 5
    ...:         print(f'f4 函数的 locals：{locals()}')
    ...:         print(f'f4 函数的 globals：{globals()}')
    ...:     return f4()
```


#### global 和 nonlocal  

global 就是在函数内可以修改 global 作用域的变量    

```python 
In [13]: a = 1

In [14]: def f1():
    ...:     a = 2
    ...: 

In [15]: a
Out[15]: 1

In [16]: def f2():
    ...:     global a
    ...:     a = 2
    ...: 

In [17]: a
Out[17]: 1

In [18]: f2()

In [19]: a
Out[19]: 2
```


nonlocal 就是把外层变量放到内层的函数的 locals() 字典中，在内层可以修改外层的变量  

在最开始 f2 函数的 locals 是没有 a 变量的  
```python 
In [426]: def f1():
     ...:     a = 1
     ...:     print(f"f1 函数的 locals 是：{locals()}")
     ...:     def f2():
     ...:         b = 2
     ...:         print(f"f2 函数的 locals 是：{locals()}")
     ...:     print(f"最后 f1 函数的 locals 是：{locals()}")
     ...:     return f2
     ...: 

In [427]: f1()
f1 函数的 locals 是：{'a': 1}
最后 f1 函数的 locals 是：{'a': 1, 'f2': <function f1.<locals>.f2 at 0x7f7d3d5b4b90>}
Out[427]: <function __main__.f1.<locals>.f2()>

In [428]: f1()()
f1 函数的 locals 是：{'a': 1}
最后 f1 函数的 locals 是：{'a': 1, 'f2': <function f1.<locals>.f2 at 0x7f7d3d5cfb90>}
f2 函数的 locals 是：{'b': 2}    # 这里没有 a  
```

加了 nonlocal 以后，内层的 locals 就有了 a 变量  

```python 
In [429]: def f1():
     ...:     a = 1
     ...:     print(f"f1 函数的 locals 是：{locals()}")
     ...:     def f2():
     ...:         nonlocal a
     ...:         b = 2
     ...:         print(f"f2 函数的 locals 是：{locals()}")
     ...:     print(f"最后 f1 函数的 locals 是：{locals()}")
     ...:     return f2
     ...: 

In [430]: f1()
f1 函数的 locals 是：{'a': 1}
最后 f1 函数的 locals 是：{'a': 1, 'f2': <function f1.<locals>.f2 at 0x7f7d35594440>}
Out[424]: <function __main__.f1.<locals>.f2()>

In [431]: f1()()
f1 函数的 locals 是：{'a': 1}
最后 f1 函数的 locals 是：{'a': 1, 'f2': <function f1.<locals>.f2 at 0x7f7d3d5cf0e0>}
f2 函数的 locals 是：{'b': 2, 'a': 1}    # 这里有了 a 变量  
``` 

通过 nonlocal 在内层函数修改了变量以后，完成变量的值还是保持不变  

```python 
In [432]: def f1():
     ...:     a = 1
     ...:     print(f"f1 函数的 locals 是：{locals()}")
     ...:     def f2():
     ...:         nonlocal a
     ...:         b = 2
     ...:         a = 3
     ...:         print(f"f2 函数的 locals 是：{locals()}")
     ...:     print(f"最后 f1 函数的 locals 是：{locals()}")
     ...:     return f2
     ...: 

In [433]: f1()
f1 函数的 locals 是：{'a': 1}
最后 f1 函数的 locals 是：{'a': 1, 'f2': <function f1.<locals>.f2 at 0x7f7d3d5b4d40>}
Out[421]: <function __main__.f1.<locals>.f2()>

In [434]: f1()()
f1 函数的 locals 是：{'a': 1}
最后 f1 函数的 locals 是：{'a': 1, 'f2': <function f1.<locals>.f2 at 0x7f7d4df77560>}   # 在这里，外层 a 还是 1 
f2 函数的 locals 是：{'b': 2, 'a': 3}   # 但是在内层，a 已经是 3 了  
```


#### sorted 函数  

默认升序。可以通过 reverse=True，改为降序  

```python 
In [1]: l = [(3, 'cat'), (1, 'bag'), (2, 'apple')]

In [2]: sorted(l, key=lambda x: x[0])
Out[2]: [(1, 'bag'), (2, 'apple'), (3, 'cat')]

In [3]: sorted(l, key=lambda x: x[1])
Out[3]: [(2, 'apple'), (1, 'bag'), (3, 'cat')]
```


#### map 类  

```python 
In [14]: list(map(abs, [-2, -1, 0, 2, 5]))
Out[14]: [2, 1, 0, 2, 5]

In [15]: def my_square(x):
    ...:     return x ** 2

In [16]: list(map(my_square, [-2, -1, 0, 2, 5]))
Out[16]: [4, 1, 0, 4, 25]
```

```python 
list(map(lambda x: x ** 2, [i for i in range(5)]))  
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

In [12]: li = [1, 2, 3, 4, 5]

In [13]: reduce(lambda x, y: x + y, li)
Out[13]: 15

先 1 + 2，再 3 + 3，再 6 + 4 等等  
```

#### partial 函数  

partial(函数，参数)，partial 函数，把参数绑定到函数上。  


#### [property 类](https://docs.python.org/zh-cn/3/library/functions.html?highlight=property#property)   

用在封装变量上。    

一般通过装饰器使用。    

fget 就是 function get，就是要有一个 get function。   




### random 模块  

随机采样  
```python 
random.sample(c_groups_result_list, k=1042)   
```


### pathlib    

#### 读取文件  

```python 
img_filenames = sorted(Path(img_base_dir).glob('*.jpg'))
annotation_filenames = sorted(Path(annotation_base_dir).glob('*.txt'))
```


#### 删除文件   

```python 
In [1]: import os

In [2]: from pathlib import Path

In [3]: for file in Path('.').glob('*.xml'):
   ...:     os.remove(file)   
```

多层目录删除文件  
```python 
In [4]: for root, dirs, files in os.walk('./'):
   ...:     for file in files:
   ...:         if file.endswith('.xml'):
   ...:             os.remove('.xml')
```


#### 获取路径和文件名  

```python 
In [1]: from pathlib import PurePath, Path

In [2]: annotation_filenames = sorted(Path('./txt_result/').glob('*.txt'))

In [3]: for name in annotation_filenames:
   ...:     print(name)
   ...: 
txt_result/feedback1_0001.txt
txt_result/feedback1_0004.txt

In [5]: for name in annotation_filenames:
   ...:     print(PurePath(name).name)
   ...: 
feedback1_0001.txt
feedback1_0004.txt

In [6]: for name in annotation_filenames:
   ...:     print(PurePath(name).parent)
   ...: 
txt_result
txt_result
```


### os  

#### os.makedirs()  

```python 
import os 

# 创建文件夹，如果文件夹已存在，会报错 FileExistsError  
os.makedirs('文件夹名')  

# 创建文件夹，文件夹存在不报错  
os.makedirs('文件夹名', exist_ok=True)  
```

#### os.path  

```python 
In [441]: import os

In [442]: path = "work/v13/危机预警.csv"

In [443]: path
Out[443]: 'work/v13/危机预警.csv'

In [444]: dir_name = os.path.dirname(path)

In [445]: dir_name
Out[445]: 'work/v13'

In [446]: file_name = os.path.basename(path)

In [447]: file_name
Out[447]: '危机预警.csv'

In [448]: os.path.splitext(file_name)
Out[448]: ('危机预警', '.csv')

In [449]: os.path.splitext(file_name)[0]
Out[449]: '危机预警'

In [450]: os.path.splitext(file_name)[1]
Out[450]: '.csv'
```


#### 获取当前路径  

```python 
os.getcwd()
```

#### 通过命令复制文件   

```python 
In [1]: import os

In [2]: with open('/home/crisis/nielsen/video/xhs_name_to_task_id.txt') as f:
   ...:     video_names = f.readlines()
   ...:     for video_name in video_names:
   ...:         video_name = video_name.split(':')[0]
   ...:         dest_dir = f'/home/crisis/nielsen/video_frames/198/{video_name}'
   ...:         if not os.path.exists(dest_dir):
   ...:             os.mkdir(dest_dir)
   ...:         cmd = f'sshpass -p "密码" scp -P 17717 -C dingyong@b62:/home/deploy/nielsen_test/upload/{video_name}/images/* {dest_dir}/'
   ...:         os.system(cmd)
   ...:         print(f'{video_name} Done.')
```


#### 通过命令删除 3 天前的文件   

```python 
In [1]: import subprocess

In [2]: import os 

In [3]: for file in subprocess.check_output('find {}  -mtime +3'.format('/home/test/syb/hszb_backend_v2/logs'), shell=True).split():
   ...:     os.remove(file) 
```


### collections 包

#### namedtuple 函数  

```python 
In [27]: from collections import namedtuple

In [29]: Person = namedtuple('Person', ['name', 'age'])

In [30]: type(Person)
Out[30]: type

In [32]: person = Person('mayanan', 30)

In [33]: person
Out[33]: Person(name='mayanan', age=30)

In [34]: type(person)
Out[34]: __main__.Person

In [35]: person.name
Out[35]: 'mayanan'

In [36]: person.age
Out[36]: 30
```


#### ChainMap 类  

这个类型可以容纳数个不同的映射对象，然后在进行键查找操作的时候，这些对象会被当作一个整体被逐个查找，直到键被找到为止。  

```python 
import builtins
pylookup = ChainMap(locals(), globals(), vars(builtins))
```


#### defaultdict 类  

解决一键多值的问题  

```python 
In [1]: from collections import defaultdict

In [2]: d = defaultdict(list)  # d 就是一个字典，字典的值是 list  

# d['a'] 就是通过键取值  
In [3]: d['a'].append(1)  # 先取值，没有返回 list，这次是没有，所以这次是先返回一个 list，然后再 append  
In [4]: d['a'].append(2)  # 这次是已经取到值了，取到列表以后 append  
In [5]: d['a'].append(3)

In [6]: d
Out[6]: defaultdict(list, {'a': [1, 2, 3]})

In [7]: d['b']
Out[7]: []

In [8]: d
Out[8]: defaultdict(list, {'a': [1, 2, 3], 'b': []})

In [9]: d['b'].append(4)
In [9]: d['b'].append(5)

In [10]: d
Out[10]: defaultdict(list, {'a': [1, 2, 3], 'b': [4, 5]})


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

In [21]: d.setdefault('a', []).append(1)  # 先取值，没有，返回空列表，然后 append  

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


### bisect 包  

根据给定的数值，查找数值的索引。  

```python 
In [37]: import bisect

In [38]: li = [1, 3, 5, 7, 9, 11, 13, 15]

In [39]: bisect.bisect(li, 7)
Out[39]: 4
```


### itertools 包  

#### zip_longest  

```python 
In [21]: a = ['a', 'b', 'c', 'd']

In [22]: b = [1, 2]

In [23]: list(zip(a, b))
Out[23]: [('a', 1), ('b', 2)]

In [24]: from itertools import zip_longest

In [25]: list(zip_longest(a, b))
Out[25]: [('a', 1), ('b', 2), ('c', None), ('d', None)]

In [26]: list(zip_longest(a, b, fillvalue='42'))
Out[26]: [('a', 1), ('b', 2), ('c', '42'), ('d', '42')]
```


#### chain

差不多是拼接  

```python
In [1]: import itertools

In [2]: itertools.chain('ABC', 'DEF')
Out[2]: <itertools.chain at 0x7ff925349e10>

In [3]: list(itertools.chain('ABC', 'DEF'))
Out[3]: ['A', 'B', 'C', 'D', 'E', 'F']

In [5]: list(itertools.chain('ABC', 'DEF', 'GHI'))
Out[5]: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
```


### more_itertools 包  

#### unzip  

```python 
>>> iterable = [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
>>> letters, numbers = unzip(iterable)
>>> list(letters)
['a', 'b', 'c', 'd']
>>> list(numbers)
[1, 2, 3, 4]
```



### typing 包

#### Union 

联合类型；Union[X, Y] 的意思是，非 X 即 Y。  


### 性能分析   

#### py-spy    

通过 1 2 3 4 切换排序规则     


#### PyCharm   

如果是 Django 项目：Profile 按钮      

如果是 .py 文件：右键     


#### 多行 log   

```python 
start = time.time()
result_list = []
logger.info('aaaaaaaaaaaaaaaaaaaaaaa %.2f sec' % (time.time() - start))
for query_item in query_result:
    for data in query_item:
        data_dict = {"url": data["url"],
                     "title": data["title"],
                     "subtitle": data["talent_text"],
                     "post_time": data["post_time"],
                     "author": data["author"]
                     }
        result_list.append(data_dict)
logger.info('bbbbbbbbbbbbbbbbbbbbb %.2f sec' % (time.time() - start))
RedisConnect.cache.rpush(search_word_md5, json.dumps(result_list))
RedisConnect.cache.expire(search_word_md5, time=60*60*24)
logger.info('cccccccccccccccccccc %.2f sec' % (time.time() - start))
```


```python 
```

### 非 Python  


#### 获取图像宽高   

`pip install opencv-python`     

```python 
import cv2   

img = cv2.imread(img_path)  
height = img.shape[0]
width = img.shape[1]
depth = img.shape[2]
```

```python 
In [1]: import cv2

In [2]: img = cv2.imread("./7070057012599491848_0000.jpg")

In [3]: img.shape
Out[3]: (1280, 720, 3)
```



#### pip 相关   

查看帮助：`pip --help`     
设置超时时间：`pip --timeout=100 install label-studio` (默认 15 秒)   
查看当前 pip 源：`pip config list`  


#### log 代码  

```python 
import logging
from importlib import reload
reload(logging)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, datefmt='%I:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
```


#### 启动虚拟环境的 ipython  

```python 
/home/test/anaconda3/envs/reci/bin/ipython
```


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


#### or 和 and  

**or 找第一个真的，and 找第一个假的**  

这本来就是 and 和 or 的字面意思，and 是都为真才返回真，所以找到一个假的，那就不用找别的了，就是假。  

or 也是，有一个为真就为真，所以找第一个为真的。  

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

参数就是输入，返回值就是输出。上下文就是外部可见的东西。  

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


[super()](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/).\_\_init__(make, model, year)  

就是调用父类的初始化方法，使得子类拥有父类初始化方法中的属性，说白了就是把父类中的初始化方法中的代码复制到了子类的初始化方法中，如果不写 super，子类的初始化方法中没有父类定义的这些属性，因为子类方法会覆盖父类的同名方法。  


# 《Effective Python》   

### 第 2 条 遵循 PEP8 风格指南  



