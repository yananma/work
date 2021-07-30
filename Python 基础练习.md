
#### 12、 题目：输入一行字符，分别统计出其中英文字母、空格、数字和其它字符的个数。

```python 
import re

s = input('请输入一串字符：')
letter, space, number, other = 0, 0, 0, 0
for char in s:
    if bool(re.match(r'[1-9]', char)):
        number += 1
    elif bool(re.match('\w', char)):
        letter += 1
    elif bool(re.match(' ', char)):
        space += 1
    else:
        other += 1
print(f'中英文字母{letter}个', f'空格{space}个', f'数字{number}个', f'其他字符{other}个')
```


#### 11、 题目：将一个正整数分解质因数。例如：输入 90,打印出 90=2\*3\*3*5。

```python 
# 质因数一定是在 2 到 sqrt(n) 之间的数字，先限定范围 2 到 (m + 1)
# 遇到余 i 等于 0 的数字，说明 i 是 n 的质因数
# 用 n 除以 i 得到商
# 把商当做新的 n，重复上面的步骤
# 如果没有了余 i 等于 0 的数字，就保存商，结束循环

from math import sqrt

n = int(input('请输入一个数字：'))
k = n
l = []
while True:
    m = int(sqrt(n))
    flag = False  # 是否有被整除的数
    for i in range(2, m + 1):
        if n % i == 0:
            flag = True
            n = n / i
            l.append(i)
            break
    if flag == False:
        l.append(int(n))
        break
print(l)

print(f"{k}={('*'.join('{}' for _ in range(len(l)))).format(*l)}")
```


#### 10、 题目：打印出所有的"水仙花数"，所谓"水仙花数"是指一个三位数，其各位数字立方和等于该数本身。例如：153是一个"水仙花数"，因为153=1的三次方＋5的三次方＋3的三次方。

```python 
for n in range(100, 1000):
    i = n // 100  # 百位 
    j = n // 10 % 10  # 十位
    k = n % 10  # 个位
    if n == i ** 3 + j ** 3 + k ** 3:
        print(n)
```


#### 9、题目：判断101-200之间有多少个素数，并输出所有素数。

```python 
from math import sqrt

l = []
for i in range(101, 200):
    m = int(sqrt(i))  
    for j in range(2, m + 1):    # 这里加 1 是因为 int 有向下取整的功能  
        if i % j == 0:
            break
    else:
        l.append(i)

print(l)
print(len(l))
```


#### 8、题目：暂停一秒输出，并格式化当前时间。 

```python 
import time, datetime

time.sleep(1)
TIME = datetime.datetime.now()
print(TIME.strftime('%Y.%m.%d %H:%M:%S'))    # strftime：string format time
```


#### 7、题目：输出 9 * 9 乘法口诀表。

```python 
for i in range(10):
    print(i)
    for j in range(1, i + 1):
        print(f'{j}x{i}={i*j}', end='\t')
    print()
```


#### 6、题目：将一个列表的数据复制到另一个列表中。

方法 1：  
```python 
l1 = [1, 2, 3]
l2 = l1[:]
print(id(l1))
print(id(l2))
```

方法 2:
```python 
import copy

l1 = [1, 2, 3]
l2 = copy.copy(l1)
```

方法 3：  
```python 
l1 = [1, 2, 3]
l2 = []
for i in range(len(l1)):
    l2.append(l1[i])
```

方法 4：  
```python 
l1 = [1, 2, 3]
l2 = [i for i in l1] 
```

方法 5：  
```python 
l1 = [1, 2, 3]
l2 = []
l2.extend(l1)
```

方法 6：  
```python 
l1 = [1, 2, 3]
l2 = l1 * 1
```


#### 5、题目：斐波那契数列。

```python
class Solution:
    def fibonacci(self, n):
        if n == 0 or n == 1:
            return n
        fib0, fib1 = 0, 1
        for i in range(n - 1):
            fib0, fib1 = fib1, fib0 + fib1
        return fib1

solution = Solution()
print(solution.fibonacci(3))
```


#### 4、题目：输入三个整数 x,y,z，请把这三个数由小到大输出。

```python 
while True:
    x = int(input('x:'))
    y = int(input('y:'))
    z = int(input('z:'))
    l = [x, y, z]
    l.sort()
    break
```


#### 3、题目：一个整数，它加上 100 后是一个完全平方数，再加上 168 又是一个完全平方数，请问该数是多少？

```python 
from math import sqrt

x = 0
while True:
    if int(sqrt(x + 100)) == sqrt(x + 100) and int(sqrt(x + 268)) == sqrt(x + 268):    # int 有向下取整的功能  
        print(x)
        break
    else:
        x += 1
```

#### 2、题目：企业发放的奖金根据利润提成。利润(I)低于或等于 10 万元时，奖金可提 10%；利润高于 10 万元，低于 20 万元时，低于 10 万元的部分按 10% 提成，高于 10 万元的部分，可提成 7.5%；20 万到 40 万之间时，高于 20 万元的部分，可提成 5%；40 万到 60 万之间时高于 40 万元的部分，可提成 3%；60 万到 100 万之间时，高于 60 万元的部分，可提成 1.5%，高于 100 万元时，超过 100 万元的部分按 1% 提成，从键盘输入当月利润 I，求应发放奖金总数？

方法 1：  
```python 
# -*- coding: UTF-8 -*-

while True:
    I = input('请输入当月利润(万元):')
    if I == 'q':
        break
    I = int(I)
    assert I > 0
    if I <= 10:
        bonus = I * 0.1
    elif 10 < I <= 20:
        bonus = 10 * 0.1 + (I - 10) * 0.075
    elif 20 < I <= 40:
        bonus = 10 * 0.1 + (20 - 10) * 0.075 + (I - 20) * 0.05
    elif 40 < I <= 60:
        bonus = 10 * 0.1 + (20 - 10) * 0.075 + (40 - 20) * 0.05 + (I - 40) * 0.03
    elif 60 < I <= 100:
        bonus = 10 * 0.1 + (20 - 10) * 0.075 + (40 - 20) * 0.05 + (60 - 40) * 0.03 + (I - 60) * 0.015
    elif 100 < I:
        bonus = 10 * 0.1 + (20 - 10) * 0.075 + (40 - 20) * 0.05 + (60 - 40) * 0.03 + (100 - 60) * 0.015 + (I - 100) * 0.01

    print(bonus)
```

方法 2：  
```python 
i = int(input('净利润:'))
arr = [100, 60, 40, 20, 10, 0]
rat = [0.01, 0.015, 0.03, 0.05, 0.075, 0.1]
r = 0
for idx in range(0, 6):
    if i > arr[idx]:
        r += (i - arr[idx]) * rat[idx]
        print((i - arr[idx]) * rat[idx])
        i = arr[idx]
        
print(r)
```


#### 1、题目：有四个数字：1、2、3、4, 5，能组成多少个互不相同且无重复数字的三位数？各是多少？

```python
v_list = [1, 2, 3, 4]
count = 0

for i in v_list:
    for j in v_list:
        for k in v_list:
            if (i != j) and (i != k) and (j != k):
                print(f'{i}{j}{k}')
                count += 1

print(count)
```
