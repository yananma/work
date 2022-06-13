
爱玛后端正式：b66，/home/deploy/aima_monitor_backend   

环境是/home/deploy/aima_monitor_backend_env/   

日志在/var/log/nginx/backend.aimatech_access.log或者/var/log/nginx/backend.aimatech_error.log   

更新前端sh /home/deploy/scripts/update_aimatech_front.sh update   

更新后端sh /home/deploy/scripts/manage_aimatech_backend.sh update   


更新话题播放量定时任务   

```sql
*/10 * * * * cd /home/deploy/aima_monitor_backend &&  /home/deploy/aima_monitor_backend_env/bin/python manage.py topic_play_quantity --settings aima_monitor_backend.settings-product &>> logs/topic_play_quantity.log &
```
