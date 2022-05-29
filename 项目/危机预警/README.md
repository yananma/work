
### 正式环境 

b25 正式环境 python：/home/deploy/.crisis/bin/python    
查看 pip：/home/deploy/.crisis/bin/pip    
查看 pip 版本：/home/deploy/.crisis/bin/pip --version     
危机预警系统后端 b25 /home/deploy/crisis_admin    
危机预警nohup /home/deploy/.crisis/bin/python manage.py runserver 0:6085 --settings=crisis_admin.settings_new_product &>>logs/crisis_admin.log &    


### 测试环境  

测试环境 python：/home/test/testenv/bin/python    
测试服务器：nohup /home/test/testenv/bin/python manage.py runserver 0:17782 --settings crisis_admin.settings_new_product &>> logs/debug.log &     

跑微博粉丝数命令：/home/test/testenv/bin/python -u /home/test/syb/crisis_admin/manage.py fill_empty_account_id --last 96 --end 2022-05-23 14:43:00 --settings=crisis_admin.settings_new_product   

`*/30 * * * * cd /home/test/syb/crisis_admin && /home/test/testenv/bin/python manage.py fill_empty_account_id --last 1 --settings=crisis_admin.settings_new_product &`   

查看更新粉丝数日志：`tail -f /home/test/syb/crisis_admin/logs/fill_empty_account_id.log`   


# 报错  

### file_path 报错  

utils/changcheng_short_video.py 中的 changcheng_short_video_export_word_files 函数，是不是没有调用 write_to_file 函数。     



