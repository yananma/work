
#### 学习语言的最佳方式是上手实践，建议您边阅读本教程，边在 Python 解释器中练习。  

这个教程介绍了 Python 语言和系统的基本概念和功能。最好在阅读的时候准备一个 Python 解释器进行练习。所有的例子都是相互独立的。  

这个教程介绍了 Python 中最值得注意的功能。  

Python 是一种解释型语言，不需要编译和链接，可以节省大量开发时间。它的解释器实现了交互式操作，轻而易举地就能试用各种语言功能。  

Python 程序简洁、易读，通常比实现同种功能的 C、C++、Java 代码短很多。  


### 2、Python 解释器  

主提示符通常用三个大于号（>>>）表示；输入连续行时，显示 次要提示符，默认是三个点（...）。  

Python 模块也可以当作脚本使用。输入：python -m module [arg] ...，会执行 module 的源文件。  

解释器读取命令行参数，把脚本名与其他参数转化为字符串列表存到 sys 模块的 argv 变量里。执行 import sys，可以导入这个模块，并访问该列表。该列表最少有一个元素；未给定输入参数时，sys.argv[0] 是空字符串。  

编码：`# -*- coding: encoding -*-`  

`help(list)`  


### 3、Python 速览  

```python 
>>> print('C:\some\name')  # here \n means newline!
C:\some
ame
>>> print(r'C:\some\name')  # note the r before the quote
C:\some\name
```

注意，-0 和 0 一样，因此，负数索引从 -1 开始。  

```python
>>> s = 'supercalifragilisticexpialidocious'
>>> len(s)
34  
```

字符串是序列类型。  

列表相加  
```python
>>> [1, 2] + [3, 4]
[1, 2, 3, 4]
```

division always returns a floating point number  

如果不希望前置 \ 的字符转义成特殊字符，可以使用 原始字符串，在引号前添加 r 即可  

合并多个变量，或合并变量与字面值，要用 +  

索引可以提取单个字符，切片提取子字符串。  

-0 和 0 一样，因此，负数索引从 -1 开始。  

输出结果包含切片开始，但不包含切片结束。  

右表达式在赋值前就已经求值了。右表达式求值顺序为从左到右。(可以理解斐波那契数列的最后的交换赋值)  

print 函数输出的内容更简洁易读，它会省略两边的引号，并输出转义后的特殊字符  

print() 函数输出给定参数的值。它能处理多个参数，包括浮点数与字符串。它输出的字符串不带引号，且各参数项之间会插入一个空格，这样可以实现更好的格式化操作。  

```python 
>>> i = 256*256
>>> print('The value of i is', i)
The value of i is 65536  
```

关键字参数 end 可以取消输出后面的换行, 或用另一个字符串结尾  

`print(a, end=',')`  


### 4、其他流程控制工具  

break 用于跳出最近的 for 或 while 循环。  

continue 表示继续执行循环的下一次迭代。  

pass 语句不执行任何操作。语法上需要一个语句，但程序不实际执行任何动作时，可以使用该语句，可以用作函数或条件子句的占位符。  

match 语句接受一个表达式并将它的值与以一个或多个 case 语句块形式给出的一系列模式进行比较。  

函数内的第一条语句是字符串时，该字符串就是文档字符串，也称为 docstring。利用文档字符串可以自动生成在线文档或打印版文档，还可以让开发者在浏览代码时直接查阅文档；**Python 开发者最好养成在代码中加入文档字符串的好习惯。**  

引用变量时，首先，在局部符号表里查找变量，然后，是外层函数局部符号表，再是全局符号表，最后是内置名称符号表。因此，尽管可以引用全局变量和外层函数的变量，但最好不要在函数内直接赋值。（除非是 global 语句定义的全局变量，或 nonlocal 语句定义的外层函数变量）（global 后面接的是全局变量，nonlocal 后面接的是外层变量，作用是内层可以赋值）。  

在调用函数时会将实际参数（实参）引入到被调用函数的局部符号表中；因此，实参是对象的引用。  

函数定义在当前符号表中把函数名与函数对象关联在一起。解释器把函数名指向的对象作为用户自定义函数。还可以使用其他名称指向同一个函数对象，并访问访该函数。  

return 语句返回函数的值。return 语句不带表达式参数时，返回 None。函数执行完毕退出也返回 None。   

```python 
In [31]: def f():
    ...:     return None
    ...: 

In [32]: f()

In [33]: print(f())
None
```

方法是“从属于”对象的函数。  

默认值只计算一次。默认值为列表、字典或类实例等可变对象时，会产生与该规则不同的结果。  
```python 
In [6]: def f(a, L=[]):
   ...:     L.append(a)
   ...:     return L
   ...: 

In [7]: print(f(1))
[1]

In [8]: print(f(2))
[1, 2]

In [9]: print(f(3))
[1, 2, 3]

In [10]: print(f([4, 5]))
[1, 2, 3, [4, 5]]

In [11]: def f(a, L=None):
    ...:     if L == None:
    ...:         L = []
    ...:     L.append(a)
    ...:     return L
    ...: 

In [12]: print(f(1))
[1]

In [13]: print(f(2))
[2]

In [14]: print(f(3))
[3]

In [15]: print(f([4, 5]))
[[4, 5]]
```

如果这些参数不是独立的，则要在调用函数时，用 * 操作符把实参从列表或元组解包出来  
```python 
>>> list(range(3, 6))            # normal call with separate arguments
[3, 4, 5]
>>> args = [3, 6]
>>> list(range(*args))            # call with arguments unpacked from a list
[3, 4, 5]
```

同样，字典可以用 ** 操作符传递关键字参数  
```python 
>>> def parrot(voltage, state='a stiff', action='voom'):
...     print("-- This parrot wouldn't", action, end=' ')
...     print("if you put", voltage, "volts through it.", end=' ')
...     print("E's", state, "!")
...
>>> d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
>>> parrot(**d)
-- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !
```


lambda 关键字用于创建小巧的匿名函数。  

Lambda 函数可用于任何需要函数对象的地方。在语法上，匿名函数只能是单个表达式。  

可以把匿名函数用作传递的实参。  

```python 
>>> pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
>>> pairs.sort(key=lambda pair: pair[1])
>>> pairs
[(4, 'four'), (1, 'one'), (3, 'three'), (2, 'two')]
```

函数注解：标注 以字典的形式存放在函数的 \_\_annotations__ 属性中，并且不会影响函数的任何其他部分。 形参标注的定义方式是在形参名后加冒号，后面跟一个表达式，该表达式会被求值为标注的值。 返回值标注的定义方式是加组合符号 ->，后面跟一个表达式，该标注位于形参列表和表示 def 语句结束的冒号之间。  

```python
>>> def f(ham: str, eggs: str = 'eggs') -> str:
...     print("Annotations:", f.__annotations__)
...     print("Arguments:", ham, eggs)
...     return ham + ' and ' + eggs
...
>>> f('spam')
Annotations: {'ham': <class 'str'>, 'return': <class 'str'>, 'eggs': <class 'str'>}
Arguments: spam eggs
'spam and eggs'
```

编码风格  


### 5、数据结构  

insert、remove、sort 等方法只修改列表，不输出返回值——返回的默认值为 None。  

列表推导式创建列表的方式更简洁。常见的用法为，对序列或可迭代对象中的每个元素应用某种操作，用生成的结果创建新的列表；或用满足特定条件的元素创建子序列。  

列表推导式的方括号内包含以下内容：一个表达式，后面为一个 for 子句，然后，是零个或多个 for 或 if 子句。结果是由表达式依据 for 和 if 子句求值计算而得出一个新列表。  






### 8、错误和异常  

执行时检测到的错误称为异常。  

可以编写程序处理选定的异常。  

try 语句可以有多个 except 子句 来为不同的异常指定处理程序。 但最多只有一个处理程序会被执行。 处理程序只处理对应的 try 子句 中发生的异常，而不处理同一 try 语句内其他处理程序中的异常。except 子句 可以用带圆括号的元组来指定多个异常。  







