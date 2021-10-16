
#### 学习语言的最佳方式是上手实践，建议您边阅读本教程，边在 Python 解释器中练习。  

这个教程介绍了 Python 语言和系统的基本概念和功能。最好在阅读的时候准备一个 Python 解释器进行练习。所有的例子都是相互独立的。  

这个教程介绍了 Python 中最值得注意的功能。  

Python 是一种解释型语言，不需要编译和链接，可以节省大量开发时间。它的解释器实现了交互式操作，轻而易举地就能试用各种语言功能。  

Python 程序简洁、易读，通常比实现同种功能的 C、C++、Java 代码短很多。  


#### Python 解释器  

主提示符通常用三个大于号（>>>）表示；输入连续行时，显示 次要提示符，默认是三个点（...）。  

Python 模块也可以当作脚本使用。输入：python -m module [arg] ...，会执行 module 的源文件。  

解释器读取命令行参数，把脚本名与其他参数转化为字符串列表存到 sys 模块的 argv 变量里。执行 import sys，可以导入这个模块，并访问该列表。该列表最少有一个元素；未给定输入参数时，sys.argv[0] 是空字符串。  

编码：`# -*- coding: encoding -*-`  

`help(list)`  


#### Python 速览  

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

