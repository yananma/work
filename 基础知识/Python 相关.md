
#### 代码怎么想的就怎么写，不要怕。  

#### 文档，每天读一点，有个印象，遇到能想起来，到时候再深入学。   

`dir(dict)`  


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


#### 

