

## 正式环境 git pull 之前要在群里说一声   

正式项目路径：```b66  /home/deploy/mx_tools```  

日志`/home/deploy/mx_tools/log/tools.log`    

python路径```/home/deploy/mx_tools_env/bin/python```   

pip `/home/deploy/mx_tools_env/bin/pip`

备份重启方式`source  /home/deploy/mx_tools_env/bin/activate && sh /home/deploy/scripts/update_tools.sh update`



## 测试环境

浏览器用 112.*.*.* 访问    

Python: `/home/dingyong/.venv/x_mx_tools/bin/python`   

路径：`/home/dingyong/mayanan/mx_tools`   


# 报错  

### 测试启动项目报错：IOError: [Errno 13] Permission denied: '/home/deploy/deploy_env/bin/activate_this.py' No handlers could be found for logger "sentry.errors"

在 mx_tools/wsgi.py 中注释掉第 18 行 `execfile(activate_this, dict(__file__=activate_this))`    


