
51 服务器   

端口 8399   

`conda activate hszb36`

`cd /home/test/syb/hszb_backend_v2`  

`nohup python manage.py runserver 0:8399 &>> logs/backend.log &`    

`tail -f logs/backend.log`   

OSError: [Errno 23] Too many open files in system: '/home/test/syb/hszb_backend_v2/templates/plugins/moment' 好像是前端插件的报错，看一看有没有用到这个插件。如果没有用到就先删了试试。   
