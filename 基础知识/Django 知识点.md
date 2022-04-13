
# 知识点   

## model 相关   

#### filter 

搜索是用 filter 实现   


#### unique_together 唯一联合约束   

去重用的，好处是可以少写处理的代码。不好的地方是，如果出现上传以后很多条只存了一条，要看是不是这个唯一约束造成了覆盖。   


#### ForeignKey 查询 

ForeignKey 就是多对一，写在多的里面，比如 comment 中写 topic 字段，使用 ForeignKey。  

如果是从 Topic 查 comment（查的结果是 comment），就用 comment_set。    

```python 
topic = Topic.objects.get(id=1)   
topic.comment_set.all()   
topic.comment_set.filter()   
```


查询的时候，comment 的 topic 字段加两个下划线，就可以拿到 Topic 的字段。两个下划线和点的意思差不多，拿属性和方法。（看 PyCharm 提示）  

```python 
Comment.objects.filter(topic__title__contains='first')   

Comment.objects.filter(topic__user__username='admin')  # 跨多层关系，topic 的 user 的 username   

Topic.objects.filter(comment__up__gte=30)  # 反向关联查询    
```


#### [order_by 按时间排序](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#order-by)   

```python 
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
```


#### [distinct 去重](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#distinct)  

跨表查询的时候会有查询结果重复的问题。   



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


## 视图   

#### 获取参数   

获取 query_string 参数（也就是 url 中问号后面的参数）的方法就是使用 `request.GET.get('vid')`     


#### 解析 JsonResponse  

```python 
# json 的格式  
result_dict = {'data': img_list, 'status': 200}
return JsonResponse(result_dict)

json.loads(response.content.decode(encoding='utf-8'))['data']   
```




## [测试](https://docs.djangoproject.com/zh-hans/4.0/topics/testing/)     

测试也要配置 DJANGO_SETTINGS_MODULE    

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




# 项目实践    

## 小知识点    

### [settigns 配置](https://docs.djangoproject.com/zh-hans/4.0/ref/settings)       

#### [数据库](https://docs.djangoproject.com/zh-hans/4.0/ref/settings/#databases)   

```python 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',   # 用内网 ip  
        'PORT': '5432',
    }
}
```

#### [时区（不配置日志时间不对）](https://docs.djangoproject.com/zh-hans/4.0/ref/settings/#time-zone-1)   



#### 指定 settings   

`--settings=ZKY_Backend.settings`  




### 模型   

#### [模型字段参考](https://docs.djangoproject.com/zh-hans/4.0/ref/models/fields/)   


#### [模型 Meta 选项](https://docs.djangoproject.com/zh-hans/4.0/ref/models/options/)   


#### 创建模型，创建应用  

```python
django-admin startproject zjgdk
cd zjgdk
django-admin startapp post   
```


### 模板   

#### [url](https://docs.djangoproject.com/zh-hans/4.0/ref/templates/builtins/#url)  

`<a href="{% url 'login' %}" class="login">登录</a>`  

添加参数    
`<a href="{% url 'blog-detail' blog.id %}">查看详细</a>`   


## 大的流程   

#### Django 项目集成静态文件   

1. 在 settings.py 的 TEMPLATES 中配置 DIRS，[BASE_DIR / "templates"]  
2. 在 settings.py 中自定义一个静态文件目录：STATICFILES_DIRS = [BASE_DIR / "static",]    
3. 在项目的 urls.py 中先 from django.urls import include，导入应用的 urls `path("", include("words.urls")),`    
4. 在应用中创建 的 urls.py，在 urls.py 中配置 url   
```python 
from . import views
from django.urls import path

urlpatterns = [
    path('index', views.index, name='index'),
    path('detail', views.detail, name='detail'),
]
```
5. 在 views.py 写视图函数   
```python 
def index(request):
    return render(request, "index.html")
```
6. 替换 HTML 里的静态文件路径，加上 static      



## 其他   

#### Django 命令   

Django 命令必须要放到 management/command 包下面，在别的地方不行。   

自定义管理命令在运行独立脚本命令方面十分有用，也可用于 UNIX 的周期性 crontab 任务，或是 Windows 的定时任务。   


#### favicon   

`<link rel="shortcut icon" href="/media/dist/img/keji.png">`   


#### inpectdb   

先配置数据库，配置数据库要用内网 ip。       

`python manage.py inspectdb > inspectdb_models.py`    


#### 重命名 app   

如果没有前移数据库，也没有各种导包引入，那么就只修改文件夹名，和应用下的 apps.py 的类名和 name 类属性     



## 报错   

### django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.  

在命令中指定 settings，`--settings=ZKY_backend.settings` 或是在 PyCharm 里指定 DJANGO_SETTINGS_MODULE=ZKY_backend.settings     


### label_tool_app.RecognizeResult.video: (models.E006) The field 'video' clashes with the field 'video_id' from model 'label_tool_app.recognizeresult'.

字段名冲突，重命名其中一个字段名。     


### PyCharm 没有办法导入 Django  

复制 Django 文件夹到 External Libraries -> Remote Libraries   


### Apps aren't loaded yet.   


