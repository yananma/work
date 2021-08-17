
#### 去重  

去重在 cache_worker.py 的 LastUpdatedOrderedDict 类中  


#### country_count 和 country_post 访问很慢  

内容很多，可以自己在 views.py 里自己更改时间  

```python 
from_date = "2021-05-30"
to_date = "2021-05-30"
```

在 middleware 的 es 函数里面，设置 has_key = 0，这样就不用每次删缓存了。  


#### value 和 value_list  

value 返回字典列表。源码：`yield {names[i]: row[i] for i in indexes}`  

value_list 返回元组列表。源码：value_list 调用了 ValuesListIterable，ValuesListIterable 里调用了 results_iter，在 results_iter 里有一句 `rows = map(tuple, rows)`  


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

