
### 跑数据  

跑数据命令   
`nohup python main.py &>> command/logs/upload_to_zjgdk_20220302.log &`   

查看日志   
`tail -f backend.log`   


### 数据统计  

1. 新浪微博，community2 索引，用 entry_name="新浪微博" 

       site_name：460003194 条  
       entry_name：460005321 条  

       搜索字段为 author_id，拼接的时候要先转为字符串格式  

       一共 1923 个账号  
    
    
2. 微信，wei 索引，用 entry_name="微信"

       微信 680505173 条数据  

3. 自媒体平台账号，page 索引，用 site_name=第一列的名称，且 entry_id=第二列数字  

4. 媒体库版面，page 索引，media_id=第一列数字  

5. 舆情通，page 索引，site_name="舆情通"，且 entry_name=第一列名称  



### 修改 Excel  

1. 重新整理每一个 sheet  
2. 把配置索引、正向查询等配置信息删除  
3. 给每一个 sheet 的每一列加上表头  





### 字段  

```python 
author_name    # 文章作者  
include_time    
is_split
talent_text_hash   
post_time
text    # 原文
title
url
author   # 提出观点的专家  
author_type   # 类型，全称还是 PER  
talent_text   # 观点段落或句子  
title_hash

# 4 个保留字段  
reserve_field  ""  
author_id  -1  
reserve_type  -1  
random_num  随机数    
```









