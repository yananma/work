



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
