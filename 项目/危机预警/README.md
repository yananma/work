
b25 正式环境 python：/home/deploy/.crisis/bin/python    
查看 pip：/home/deploy/.crisis/bin/python    


危机预警系统后端 b25 /home/deploy/crisis_admin（新）    
危机预警nohup /home/deploy/.crisis/bin/python manage.py runserver 0:6085 --settings=crisis_admin.settings_new_product &>>logs/crisis_admin.log &    
测试服务器：nohup /home/test/testenv/bin/python manage.py runserver 0:17782 --settings crisis_admin.settings_new_product &>> logs/debug.log &     

