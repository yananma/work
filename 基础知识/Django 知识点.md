
## model 相关   

#### filter 

搜索是用 filter 实现   


#### unique_together 唯一联合约束   

去重用的，好处是可以少写处理的代码。不好的地方是，如果出现上传以后很多条只存了一条，要看是不是这个唯一约束造成了覆盖。   


#### ForeignKey 查询 

ForeignKey 就是多对一，写在多的多的里面，比如 comment 中写 topic 字段，使用 ForeignKey。  

查询的时候，comment 的 topic 字段加两个下划线，就可以拿到 Topic 的字段。两个下划线和点的意思差不多，拿属性和方法。  


#### 去重  

去重在 cache_worker.py 的 LastUpdatedOrderedDict 类中  


#### country_count 和 country_post 访问很慢  

内容很多，可以自己在 views.py 里自己更改时间  

```python 
from_date = "2021-05-30"
to_date = "2021-05-30"
```

在 middleware 的 es 函数里面，设置 has_key = 0，这样就不用每次删缓存了。  


#### values 和 values_list  

values 返回字典列表。源码：`yield {names[i]: row[i] for i in indexes}`  

values_list 返回元组列表。源码：value_list 调用了 ValuesListIterable，ValuesListIterable 里调用了 results_iter，在 results_iter 里有一句 `rows = map(tuple, rows)`  


#### Django 字符串拼接  

```python
from django.db.models.functions import Concat
from django.db.models import F, Q, Value, CharField

.annotate(budget=Concat(F('total_budget'), Value(' ('), F('fiscal_year'), Value(')'), output_field=CharField()))
.annotate(five_years_budget=Concat(F('next_five_years'), Value(' ('), F('fiscal_year'), Value('-'), F('fiscal_year') + 4, 
Value(')'), output_field=CharField()))   # output_field 为必填字段  
```

最后显示效果  
```json
"budget": "45.423 (2021)",
"five_years_budget": "237.75 (2021-2025)",
```


## 测试   

貌似我们的测试多的快要失去控制了。按照这样发展下去，测试代码就要变得比应用的实际代码还要多了。   

但是这没关系！ 就让测试代码继续肆意增长吧。大部分情况下，你写完一个测试之后就可以忘掉它了。在你继续开发的过程中，它会一直默默无闻地为你做贡献的。   

当你继续开发的时候，发现之前的一些测试现在看来是多余的。但是这也不是什么问题，多做些测试也不错。  

如果你对测试有个整体规划，那么它们就几乎不会变得混乱。下面有几条好的建议：  

* 对于每个模型和视图都建立单独的 TestClass  
* 每个测试方法只测试一个功能  
* 给每个测试方法起个能描述其功能的名字，测试的函数名类名可以起很长的名字     

默认的 startapp 会在新的应用程序中创建一个 tests.py 文件。如果你只有几个测试，这可能是好的，但随着你的测试套件的增长，你可能会想把它重组为一个测试包，这样你就可以把你的测试分成不同的子模块，如 test_models.py、test_views.py、test_forms.py 等。你可以自由选择任何你喜欢的组织方案。   

需要数据库的测试（即模型测试）将不会使用“实际”（生产）数据库。 将为测试创建单独的空白数据库。  

无论测试是通过还是失败，当所有测试执行完毕后，测试数据库都会被销毁。  

测试客户端是一个 Python 类，它充当一个虚拟的 Web 浏览器，允许你测试视图并以编程方式与 Django 驱动的应用程序交互。   




## 其他   

#### Django 命令   

Django 命令必须要放到 management/command 包下面，在别的地方不行。   

自定义管理命令在运行独立脚本命令方面十分有用，也可用于 UNIX 的周期性 crontab 任务，或是 Windows 的定时任务。   



