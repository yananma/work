
6、题目：将一个列表的数据复制到另一个列表中。

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


5、题目：斐波那契数列。

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


4、题目：输入三个整数 x,y,z，请把这三个数由小到大输出。

```python 
while True:
    x = int(input('x:'))
    y = int(input('y:'))
    z = int(input('z:'))
    l = [x, y, z]
    l.sort()
    break
```


3、题目：一个整数，它加上 100 后是一个完全平方数，再加上 168 又是一个完全平方数，请问该数是多少？

```python 
from math import sqrt, floor

x = 0
while True:
    if floor(sqrt(x + 100)) == sqrt(x + 100) and floor(sqrt(x + 268)) == sqrt(x + 268):
        print(x)
        break
    else:
        x += 1
```

2、题目：企业发放的奖金根据利润提成。利润(I)低于或等于 10 万元时，奖金可提 10%；利润高于 10 万元，低于 20 万元时，低于 10 万元的部分按 10% 提成，高于 10 万元的部分，可提成 7.5%；20 万到 40 万之间时，高于 20 万元的部分，可提成 5%；40 万到 60 万之间时高于 40 万元的部分，可提成 3%；60 万到 100 万之间时，高于 60 万元的部分，可提成 1.5%，高于 100 万元时，超过 100 万元的部分按 1% 提成，从键盘输入当月利润 I，求应发放奖金总数？

解法 1：  
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

解法 2：  
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


1、题目：有四个数字：1、2、3、4, 5，能组成多少个互不相同且无重复数字的三位数？各是多少？

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
