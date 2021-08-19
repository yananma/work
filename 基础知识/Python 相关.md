
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

### 字符串  

#### translate() 和 maketrans() 

```python 
In [2]: s = 'abcde'

In [4]: s.maketrans({'c': ''})
Out[4]: {99: ''}

In [6]: s.translate(str.maketrans({'c': ''}))
Out[6]: 'abde'

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

将字符串 s 中的所有命名和数字字符引用 (例如 `&gt;`, `&#62;`, `&#x3e;`) 转换为相应的Unicode字符。  

比如把 `&ldquo;` 转换成左双引号，这要就可以通过 translate() 和 maketrans() 去掉了   



### 列表  

#### 列表::切片  

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


### 函数  

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



### 其他  

#### \n \t  

\n 可能是 new line  
\t tab 制表符  


#### 多用 yield  



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




### Python 基础知识  

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



