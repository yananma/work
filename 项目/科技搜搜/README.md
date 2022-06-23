
正式环境目录：  

`/opt/zky_backend`   

日志：`tail -f logs/uwsgi.log`   

看日志命令：`cd /opt/zky_backend/ && tail -f logs/uwsgi.log`  

改完代码要重启：`/usr/local/python37/bin/uwsgi --reload logs/uwsgi.pid`   

[跑数据命令.md](https://github.com/yananma/work/blob/main/%E9%A1%B9%E7%9B%AE/%E7%A7%91%E6%8A%80%E6%90%9C%E6%90%9C/%E8%B7%91%E6%95%B0%E6%8D%AE%E5%91%BD%E4%BB%A4.md)   


### 跑漏的数据   

指定 -l 参数，跑之前多少天的数据。   

先跑基本的数据，这些跑完才能去跑别的。     

```python 
nohup cd /opt/zky_backend && /usr/local/python37/bin/python3.7 manage.py --settings=ZKY_Backend.settings upload_history_v2 -l 8 -i "kejisousou-formal" -pi "kejisousou-points-formal" -tp 4 -df "include_time" &>> /tmp/upload_history_v2_20220622.log &

nohup cd /opt/zky_backend && /usr/local/python37/bin/python3.7 manage.py --settings=ZKY_Backend.settings upload_history_v2 -l 8 -i "kejisousou-en-formal" -tp 0 -df "include_time" -uc "zky_title_md5_formal_en" -us "zky_point_sentence_md5_formal_en" -file "/opt/zky_backend/resources/docs/program/中科院外文网站.xlsx" --no-point -en &>> /tmp/upload_history_v2_en_20220622.log &
```    

跑完上面的数据，再跑预测治理。    

```python 
nohup cd /opt/ZKYYuceAndZhili && /home/deploy/anaconda3/envs/mxnlp/bin/python yuce.py --last 9 --point_index "kejisousou-points-formal" --yuce_index "kejisousou-yuce-formal-v4" --search_time_field "zky_include_time" &>> /tmp/yuce_20220623.log &

nohup cd /opt/ZKYYuceAndZhili && /home/deploy/anaconda3/envs/mxnlp/bin/python zhili.py --last 9 --point_index "kejisousou-points-formal" --zhili_index "kejisousou-zhili-formal-v3" --search_time_field "zky_include_time" &>> /tmp/zhili_20220623.log &   
``` 





