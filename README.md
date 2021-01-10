# GroupCalendar

GroupCalendar是一个简单的日程表，提供以下功能：

1. 注册后可以输入自己的日程表/课表，数据存储在线上，并可查看当前处于学期第几周

2. 创建或加入同学的小组，可通过组长学号加入

3. 小组内共享成员间的日程安排，组长可以为小组添加小组日程

   

## 运行：

```
python3 manage.py runserver 8080
```



## 在服务器上部署

```
uwsgi -d --ini calendar.ini
```

