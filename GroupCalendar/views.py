from django.http import HttpResponse
from django.shortcuts import render
from mydb.views import *

def index(request):
    context = {}
    stuid = request.GET.get("stuid")
    context['weekdaynames'] = [
        "星期一",
        "星期二",
        "星期三",
        "星期四",
        "星期五",
        "星期六",
        "星期日",
    ]
    classes = [
        "第一节课 07:50-08:35",
        "第二节课 08:40-09:25",
        "第三节课 09:45-10:30",
        "第四节课 10:35-11:20",
        "第五节课 11:25-12:10",
        "午休时间",
        "第六节课 14:00-14:45",
        "第七节课 14:50-15:35",
        "第八节课 15:40-16:25",
        "第九节课 16:45-17:30",
        "第十节课 17:35-18:20",
        "晚餐时间",
        "第十一节 19:30-20:15",
        "第十二节 20:20-21:05",
        "第十三节 21:10-21:55",
    ]
    context['courses'] = {}
    # courses = Course.table_get_course(stuid)
    # courses = Course.table_get_course('')
    for i in range(15):
        # context['courses'][classes[i]] = courses[i]
        context['courses'][classes[i]] = ["" for j in range(7)]
    context['default_courses'] = ["工程伦理", "研究生综合英语", "算法设计与分析", "高级软件工程", "软件体系结构", 
            "高级网络技术", "数据仓库与数据挖掘", "人工智能", "区块链技术", "C++面向对象技术", "深度学习实践"]
    
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')

def group(request):
    context = {}
    groupid = request.GET.get("groupid")
    context['weekdaynames'] = [
        "星期一",
        "星期二",
        "星期三",
        "星期四",
        "星期五",
        "星期六",
        "星期日",
    ]
    classes = [
        "第一节课 07:50-08:35",
        "第二节课 08:40-09:25",
        "第三节课 09:45-10:30",
        "第四节课 10:35-11:20",
        "第五节课 11:25-12:10",
        "午休时间",
        "第六节课 14:00-14:45",
        "第七节课 14:50-15:35",
        "第八节课 15:40-16:25",
        "第九节课 16:45-17:30",
        "第十节课 17:35-18:20",
        "晚餐时间",
        "第十一节 19:30-20:15",
        "第十二节 20:20-21:05",
        "第十三节 21:10-21:55",
    ]
    context['affairs'] = {}
    for i in range(15):
        context['affairs'][classes[i]] = ["" for j in range(7)]
    return render(request, 'group.html', context)
