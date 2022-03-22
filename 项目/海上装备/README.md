
51 服务器   

端口 8399   

`conda activate hszb36`

`cd /home/test/syb/hszb_backend_v2`  

`nohup python manage.py runserver 0:8399 &>> logs/backend.log &`    

`tail -f logs/backend.log`   
