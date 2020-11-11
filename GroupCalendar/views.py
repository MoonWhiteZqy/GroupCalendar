from django.http import HttpResponse
from django.shortcuts import render
from mydb.views import *

def index(request):
    context = {}
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
        "第一节课 08:00-08:45",
        "第二节课 08:55-09:40",
        "第三节课 09:55-10:40",
        "第四节课 10:50-11:35",
        "第五节课 11:45-12:30",
        "第六节课 13:30-14:15",
        "第七节课 14:25-15:10",
        "第八节课 15:25-16:10",
        "第九节课 16:20-17:05",
        "第十节课 17:15-18:00",
        "第十一节 18:30-19:15",
        "第十二节 19:25-20:10",
        "第十三节 20:20-21:05",
        "第十四节 21:10-24:00"
    ]
    context['courses'] = {}
    courses = Course.table_get_course('17307130109')
    # courses = Course.table_get_course('')
    for i in range(14):
        context['courses'][classes[i]] = courses[i]
    
    return render(request, 'index.html', context)

def login(request):
    return render(request, 'login.html')    