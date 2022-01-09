

1. 新浪微博，community2 索引，用 entry_name="新浪微博" 

       site_name：460003194 条  
       entry_name：460005321 条  

       搜索字段为 author_id，拼接的时候要先转为字符串格式  

       一共 1923 个账号，看是怎么查的，是不是也用 OR 拼接，会不会太长了  
    
    
2. 微信，wei 索引，用 entry_name="微信"

       微信 680505173 条数据  

3. 自媒体平台账号，page 索引，用 site_name=第一列的名称，且 entry_id=第二列数字  

4. 媒体库版面，page 索引，media_id=第一列数字  

5. 舆情通，page 索引，site_name="舆情通"，且 entry_name=第一列名称  


