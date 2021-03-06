
# 知识点   

## model 相关   

#### filter 

搜索是用 filter 实现   


#### 查询关键字 in  

不要用 for 循环遍历多次查询，而是用 in 一次查询。   

不好的做法，会查询很多次：   
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


#### ForeignKey 写在 comment 里，查询的时候考虑 topic 就是跨关联关系查询，比如 comment.objects.filter(topic__title__contains='first')。查询 topic 就是反向查询。比如 Topic.objects.filter(comment__up__gte=30)。意思就是查的不是它自己，而是别的东西。


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


#### [OneToOneField](https://docs.djangoproject.com/zh-hans/4.0/topics/db/examples/one_to_one/)    

```python 
class PostIsCleaned(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, unique=True)
    # 更新粉丝数，爬虫返回的 is_cleaned 的结果，0 为 false，1 为 true，默认为 1
    is_cleaned = models.IntegerField(default=1)

    class Meta:
        managed = False
        db_table = 'post_is_cleaned'
```  

数据库里应该是 3 个字段，id、post_id 和 is_cleaned。    


#### [order_by 按时间排序](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#order-by)   

如果是：order_by('-include_time')，就是新的在最上面。  

```python 
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
```


#### [distinct 去重](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#distinct)  

跨表查询的时候会有查询结果重复的问题。   


#### 返回 QuerySet 的好处是可以做到链式查询。     


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

QuerySet 没有 append 方法，要转成 list 再 append   

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


#### 获取属性值   

一般来说有两种取值方法：      

可以直接取属性的值。    
```python 
TopicPlayQuantity.objects.filter(cid=cid).order_by('include_time').last().view_count
```

函数调用用这种，可以传入字符串形式的字段名称。    

```python 
TopicPlayQuantity.objects.filter(cid=cid).order_by('include_time').values_list('view_count').[0][0]    
或   
TopicPlayQuantity.objects.filter(cid=cid).order_by('include_time').values_list('view_count').first()[0]   
不支持负数索引，如果要取最后一个，要用 last   
TopicPlayQuantity.objects.filter(cid=cid).order_by('include_time').values_list('view_count').last()[0]    
```   


#### [first](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#first)   

一版前面要写 order_by，取到值以后，如果要取其中的属性值，就直接用点儿取就行。   

```python 
TopicPlayQuantity.objects.order_by('include_time').last().view_count   
```   


#### [create](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#create)   

创建一个对象并保存。
```python  
p = Person.objects.create(first_name="Bruce", last_name="Springsteen")   
```
和：
```python 
p = Person(first_name="Bruce", last_name="Springsteen")
p.save(force_insert=True)
```
是等效的。

```python 
TopicPlayQuantity.objects.create(
    cha_name=data['ch_info']['cha_name'],
    cid=data['ch_info']['cid'],
    view_count=data['ch_info']['view_count'],
    user_count=data['ch_info']['user_count'],
    view_increment=data['ch_info']['view_count'] - TopicPlayQuantity.objects.order_by('include_time').last().view_count,
    user_increment=data['ch_info']['user_count'] - TopicPlayQuantity.objects.order_by('include_time').last().user_count,
    hash_tag_profile=data['ch_info']['hash_tag_profile'],
    desc=data['ch_info']['desc'],
    type=data['ch_info']['type'],
    is_commerce=data['ch_info']['is_commerce'],
    include_time=datetime.datetime.strptime(data['extra']['logid'][:14], "%Y%m%d%H%M%S"),
)
```


#### [update](https://docs.djangoproject.com/zh-hans/4.0/ref/models/querysets/#update)    

可以同时更新多个字段。   

```python 
Entry.objects.filter(pub_date__year=2010).update(comments_on=False, headline='This is old')   
```

```python 
import datetime
import pandas as pd
from django.core.management.base import BaseCommand
from video.models import DouyinVideo


class Command(BaseCommand):
    help = 'update interaction number'

    def handle(self, *args, **options):
        df = pd.read_excel('/home/test/syb/aima_monitor_backend/video/management/commands/data/更新video互动.xlsx')
        for i, row in df.iterrows():
            DouyinVideo.objects.filter(url=row['视频链接']).update(collect_num=row['collect_count'],
                                                               share_num=row['share_count'],
                                                               comment_num=row['comment_count'],
                                                               like_num=row['like_count'],
                                                               update_time=datetime.datetime.now())
        print('update interaction number success')
```

更新数据库为 NULL，在 ORM 里就是赋值为 None。   


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


#### group by  

```python 
from django.db import models
from django.db.models.functions import TruncDate

from notice.models import Post


sql_res = list(Post.objects.filter(noise_rank=0)
               .annotate(posttime_date=TruncDate('posttime'))
               .values('facetid', 'posttime_date', 'status')
               .annotate(count=models.Count(models.Value(1, models.IntegerField())))
               .values('facetid', 'posttime_date', 'status', 'count'))
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


## 模板  

#### [verbatim](https://docs.djangoproject.com/zh-hans/4.0/ref/templates/builtins/#verbatim)  

对于 {{ }} 符号，Vue 和 Django 模板语法冲突，会优先 Django 渲染，Vue 就没有办法运行，解决办法就是在代码外层添加 verbatim    



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

TIME_ZONE = 'Asia/Shanghai'   


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

#### 量太大，没有办法一次更新完的解决办法   

```python 
from notice.models import Post
from more_itertools import chunked

for batch in chunked(Post.objects.filter(domain=u'今日头条', is_clean=0, sourcetype__in=[1, 15]).force_index('idx_sourcetype').values_list('postid', flat=True), 10000):
    Post.objects.filter(postid__in=batch).force_index(key=True).update(is_clean=None)
```  


### 模板   

#### [url](https://docs.djangoproject.com/zh-hans/4.0/ref/templates/builtins/#url)  

`<a href="{% url 'login' %}" class="login">登录</a>`  

添加参数    
`<a href="{% url 'blog-detail' blog.id %}">查看详细</a>`   


## 大的流程   


#### 上传文件  

```html
{% extends "base.html" %}

{% block content %}
    <div class="row" style="margin-left: 3%; margin-top: 1%">
        <form method="post" id="my_form" enctype="multipart/form-data" action="/（目标接口）" >
            <div class="custom-file">
                <label for="photoCover">请选择文件:</label>
                <input type="file" id="csvfile" name="csvfile" style="width: 23%">
                <button id="btn_save" type="button" onclick="checkData()" style="background-color: #0066cc; margin-top: 10px; color: white; border: none; width: 5%; height: 35px; font-size: 16px">上传</button>
            </div>
        </form>
        <h3 style="color:{{ msg_color }}">{{ msg }}</h3>
    </div>


<script>
    function checkData() {
        let csv_file = $("#csvfile").val()
        if(!csv_file) {
            alert("请先选择文件！");
            return false;
        }
        let strs = csv_file.split('.');
        if((strs[strs.length-1] !== "xlsx")){
            alert("请上传xlsx格式的文件！");
            return false;
        }
        $("#my_form").submit();
    }
</script>
{% endblock %}
```

```python 
def do_export_changcheng_short_video(request):
    """长城短视频"""
    if request.method == 'POST':
        try:
            upload_dir = os.path.join(settings.BASE_DIR, 'static', 'upload', 'changcheng_short_video', 'upload')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            upload_file = request.FILES.get('csvfile')
            file_obj = open(os.path.join(upload_dir, upload_file.name), 'wb')
            for chunk in upload_file.chunks():
                file_obj.write(chunk)
            file_obj.close()
            return render(request, 'notice/short_video_export_data.html', {'msg': '上传成功', 'msg_color': 'green'})
        except Exception as e:
            return render(request, 'notice/short_video_export_data.html', {'msg': '上传失败', 'msg_color': 'red'})        
    return render(request, 'notice/short_video_export_data.html', locals())
```

直接接收上传的文件，而不是写入再读取    

这里是 Python2，read 完以后，就是 str     

```python 
upload_file = request.FILES.get('json_file').read()
lines = upload_file.splitlines()
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
    # response['Content-Disposition'] = 'attachment;filename="%s"' % quote(file_name.split('_')[1].encode('utf-8'))  # 可以指定导出的文件的名字    
    # response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)  # 测试不成功，也不知道为什么。
    return response
```

#### office 报错文件已损坏，无法打开  

保存格式从 docx 改成 doc    


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

#### [Django 命令](https://docs.djangoproject.com/zh-hans/4.0/howto/custom-management-commands/)   

Django 命令必须要放到 management/**commands**(有一个 s) 包下面，在别的地方不行。   

如果找不到命令，还有一个原因可能就是配置的 DJANGO_SETTINGS_MODULE=aima_monitor_backend **.settings**没有写后面的 .settings    

自定义管理命令在运行独立脚本命令方面十分有用，也可用于 UNIX 的周期性 crontab 任务，或是 Windows 的定时任务。   

如果在参数里指定了 type=int，如果传了小数就会报错。    

```python 
from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
```


#### PyCharm 配置运行命令  

先右键 run，然后配置。    

Script Path：C:\Users\mx\PycharmProjects\aima_monitor_backend\manage.py    
Parameters：命令名   

Environment variables：DJANGO_SETTINGS_MODULE=aima_monitor_backend.settings   


#### PyCharm 同时运行同一个命令   

不能再两个 PyCharm 窗口中打开同一个项目，可以把脚本复制出来，换一个名字，运行就可以了。     


#### favicon   

`<link rel="shortcut icon" href="/media/dist/img/keji.png">`   


#### inspectdb    

先配置数据库，配置数据库要用内网 ip。       

```python
python manage.py inspectdb > inspectdb_models.py
```       

指定数据库   

```python 
/home/test/testenv/bin/python manage.py inspectdb --database notice   
```


#### 重命名 app   

如果没有前移数据库，也没有各种导包引入，那么就只修改文件夹名，和应用下的 apps.py 的类名和 name 类属性     



## 报错   

### django.core.exceptions.ImproperlyConfigured: Requested setting DATABASES, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.（4 次）  

在命令中指定 settings，`--settings=ZKY_backend.settings` 或是在 PyCharm 里指定 DJANGO_SETTINGS_MODULE=ZKY_backend.settings     

如果是 python 脚本（也就是说不是 django 脚本），要在前面设置环境变量。要写到导入 settings 前面。   

```python 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zjgdk.settings")
from django.conf import settings
``` 


### ValueError: Cannot use None as a query value (3 次)   

看查询语句，查询字段中有的查询值是 None   


### Access denied，没有权限看 "192.169.241.%"（2 次）  

看配置是不是把 database 配置成了表。database 应该配置库。    


### 网页报错 503  

看看服务器是不是挂了    


### label_tool_app.RecognizeResult.video: (models.E006) The field 'video' clashes with the field 'video_id' from model 'label_tool_app.recognizeresult'.

字段名冲突，重命名其中一个字段名。     


### PyCharm 没有办法导入 Django  

复制 Django 文件夹到 External Libraries -> Remote Libraries   


### Can't get remote credentials for deployment server    

第一种情况：左键右下角 Interpreter -> Interpreter Settings -> 配置 Path Mapping   

第二种情况：左键右下角 Interpreter -> Interpreter Settings -> Python Interpreter 右侧齿轮 -> Show All -> 左上角第三个 icon edit -> 看 Deployment configuration -> -> ->


### MySQLdb.\_exceptions.OperationalError: (1054, "Unknown column 'nielsen_item.ocr_modify_if' in 'field list'")    

数据库中缺少字段。设计表，添加字段就可以了。      


### 测试，数据库没有 test_ 表   

在右侧大窗口，右键 -> 导出向导 -> 导出成 xlsx 格式就行 -> 新表中右侧大窗口右键 -> 导入向导。（导入不成功，不知道为什么，数据是有的，但是在原表上测试可以通过，在新表上测试就报错）     

1. 如果本来用的是正常表，而没有测试表，就自己通过导出导入实现复制表。新表叫做 test_ 。
2. 如果用的是 test_ 表，没有 test_test_ 表，就先改配置改成正常表。或者再复制一张表。     


### Apps aren't loaded yet.   


