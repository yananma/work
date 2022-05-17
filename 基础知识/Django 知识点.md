
# 知识点   

## model 相关   

#### filter 

搜索是用 filter 实现   


#### 查询关键字 in  

不要用 for 循环遍历多次查询，而是用 in 一次查询。   

不好的做法，会查询很多次，如果数量多了以后：   
```python 
result = []   
for url in query_urls:
    one_result = Post.objects.filter(url=url).values()
    result.extend(one_result)   
```

好的做法：   
```python 
result = Post.objects.filter(url__in=query_urls).values()       
```


#### unique_together 唯一联合约束   

去重用的，好处是可以少写处理的代码。不好的地方是，如果出现上传以后很多条只存了一条，要看是不是这个唯一约束造成了覆盖。   


#### ForeignKey 查询 

跨关联关系查询最重要的方法是看 PyCharm 提示   

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



#### [values](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#values)   

返回结果为列表套字典格式的 QuerySet：   

```python 
>>> Blog.objects.values('id', 'name')
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
```  

values 返回 QuerySet 形式的字典列表。源码：`yield {names[i]: row[i] for i in indexes}`  

```python   
RecognizeResult.objects.filter(video_id=request.GET.get('vid')).values('logo')  
```

QuerySet 转 list   

```python 
list(QuerySet)   
```


QuerySet 转 dict   

```python 
def detail_logo_view(request):
    """详细页面 logo 下拉框数据"""
    logo_list = RecognizeResult.objects.filter(video_id=request.GET.get('vid')).values('logo')
    logo_list = [item for item in logo_list]
    return JsonResponse({'data': logo_list, 'status': 200})
```

有时候从数据库里取出来的值，用 json.loads 的时候不成功，很可能是要先做把单引号 replace 成双引号。   

```python 
json.loads(logo_dict['logo'].replace("\'", "\""))
```  


#### [values_list](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#values-list)  

flat 参数。如果 True，这将意味着返回的结果是单个值，而不是一个元组。    

```python 
>>> Entry.objects.values_list('id').order_by('id')
<QuerySet[(1,), (2,), (3,), ...]>

>>> Entry.objects.values_list('id', flat=True).order_by('id')
<QuerySet [1, 2, 3, ...]>
```


values_list 返回元组列表。源码：value_list 调用了 ValuesListIterable，ValuesListIterable 里调用了 results_iter，在 results_iter 里有一句 `rows = map(tuple, rows)`  


#### [Q()查询](https://docs.djangoproject.com/zh-hans/4.0/topics/db/queries/#complex-lookups-with-q)   

有多个 filter 和 exclude 的时候，就换成 Q 查询。    

Q 表达式很长的时候，提取 Q 表达式。核心就是外层加一个括号。    

```python 
def get_detail_q_expr(search_word):
    """拼接 Q 表达式"""
    q_expr = (Q(ocr__icontains=search_word) |
               Q(flower_subtitles__icontains=search_word) |
               Q(logo__icontains=search_word) |
               Q(breed__icontains=search_word))
    return q_expr
```   


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

秘诀就是要**频繁地大量地重复地运行测试**，这样就可以把 bug 限定在一个非常非常小的范围内，消除了查找 bug 的时间，bug 没有了深度，大部分 bug 在一分钟内就可以改好。非常容易，非常愉快。    

测试节省了大量的调试代码的时间，所以可以大幅提高开发速度，可以大幅降低开发难度。通过测试，后端开发就和前端开发一样了。    

测试没有次数限制，一天运行 200 到 300 次。   

一旦停止运行，再运行，如果遇到问题，解决起来问题就难多了。    


测试证明 I have the control of the code.   

不要做一个 good debugger，debug 就是在浪费时间，要多做测试。    

测试驱动 is fun. 每次测试通过都会非常高兴。这是只做 unittest 所没有的 experience，unittest 是一种额外多做工作必须要做的工作的感觉，像刷碗一样。    

会计学，验证结果的正确性，是有两套计算，最后用两个计算的结果相减为零。测试驱动开发也是这样，是两套系统。    

一套可以信任的测试能够使代码修改变得异常简单。   

没有测试就不敢重构。没有测试敢重构吗？根本不敢。   

频繁地运行测试   
测试驱动   
每个函数至少要有一个测试。   
所有的 bug。    
测边界条件：空容器、空字符串、零、负数。   
写测试的时候，是一个破坏者的状态。测出不对来才是完成了测试。     


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


#### 上传文件  

```html
        <form method="post" id="my_form" enctype="multipart/form-data" action="/notice/do_export_changcheng_short_video" >
            <div class="custom-file">
                <label for="photoCover">请选择文件:</label>
                <input type="file" id="csvfile" name="csvfile" style="width: 23%">
                <button id="btn_save" type="button" onclick="checkData()" style="background-color: #0066cc; margin-top: 10px; color: white; border: none; width: 6%; height: 35px; font-size: 16px">上传文件</button>
            </div>
        </form>
```

```python 
def do_export_changcheng_short_video(request):
    """长城短视频"""
    if request.method == 'POST':
        upload_dir = os.path.join(settings.BASE_DIR, 'static', 'upload', 'changcheng_short_video', 'upload')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        upload_file = request.FILES.get('csvfile')
        file_obj = open(os.path.join(upload_dir, upload_file.name), 'wb')
        for chunk in upload_file.chunks():
            file_obj.write(chunk)
        file_obj.close()
    return render(request, 'notice/short_video_export_data.html', locals())
```


#### 下载文件  

```html   
<div class="row" style="margin-left: 3%; margin-top: 1%">
    <a id='download_file' class="btn btn-primary" href="/notice/download_changcheng_short_video_data">下载</a>
</div>
```


```python 
from urllib import quote  # python2   
# from urllib.parse import quote  # python3 未测试   


def download_changcheng_short_video_data(request):
    """短视频下载文件"""
    result_dir = os.path.join(settings.BASE_DIR, 'static', 'upload', 'changcheng_short_video', 'result')
    file_name = '20220512173038_5月9日长城全品牌短视频敏感信息汇总(1).xlsx'
    file_path = os.path.join(result_dir, file_name)
    file_obj = open(file_path, 'rb')
    response = FileResponse(file_obj)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % quote(file_name.encode('utf-8'))  # 成功  
    # response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)  # 测试不成功，也不知道为什么。
    return response
```



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


#### inspectdb    

先配置数据库，配置数据库要用内网 ip。       

`python manage.py inspectdb > inspectdb_models.py`    


#### 重命名 app   

如果没有前移数据库，也没有各种导包引入，那么就只修改文件夹名，和应用下的 apps.py 的类名和 name 类属性     



## 报错   

### ValueError: Cannot use None as a query value (3 次)   

看查询语句，查询字段中有的查询值是 None   


### django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.（3 次）  

在命令中指定 settings，`--settings=ZKY_backend.settings` 或是在 PyCharm 里指定 DJANGO_SETTINGS_MODULE=ZKY_backend.settings     


### label_tool_app.RecognizeResult.video: (models.E006) The field 'video' clashes with the field 'video_id' from model 'label_tool_app.recognizeresult'.

字段名冲突，重命名其中一个字段名。     


### PyCharm 没有办法导入 Django  

复制 Django 文件夹到 External Libraries -> Remote Libraries   


### Can't get remote credentials for deployment server    

第一种情况：左键右下角 Interpreter -> Interpreter Settings -> 配置 Path Mapping   

第二种情况：左键右下角 Interpreter -> Interpreter Settings -> Python Interpreter 右侧齿轮 -> Show All -> 左上角第三个 icon edit -> 看 Deployment configuration -> -> ->


### Apps aren't loaded yet.   


