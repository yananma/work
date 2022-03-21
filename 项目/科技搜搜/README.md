
正式环境目录：  

`/opt/zky_backend`   

日志：`tail -f logs/uwsgi.log`   

看日志命令：`cd /opt/zky_backend/ && tail -f logs/uwsgi.log`  

改完代码要重启：`/usr/local/python37/bin/uwsgi --reload logs/uwsgi.pid`   

