from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, reverse

# Create your views here.
from .models import CourseModel, StudentModel, AffairModel
from django.views.generic import View
from GroupCalendar import views
import json

def success(kwargs):
    res = {'status':'success'}
    if kwargs:
        for k, v in kwargs.items():
            res[k] = v
    return json.dumps(res)

def fail(kwargs):
    res = {'status':'fail'}
    if kwargs:
        for k, v in kwargs.items():
            res[k] = v
    return json.dumps(res)

def jsonify(request):
    return json.loads(request.body)

# 构建一个表格，用于存放数据
def table_construct(x, y):
    tables = []
    for i in range(x):
        table = []
        for j in range(y):
            table.append("")
        tables.append(table)
    return tables


class Course(View):
    def get_course(request):
        id = request.GET.get('stuid')
        courses = CourseModel.objects(stuid=id)
        infos = {}
        count = 0
        for course in courses:
            info = {
                'stuid':course.stuid,
                'weekday':course.weekday,
                'daytime':course.daytime
            }
            infos[count] = info
            count += 1
        if len(infos) > 0:
            return HttpResponse(success(infos))
        return HttpResponse(fail())

    def table_get_course(id):
        courses = CourseModel.objects(stuid = id)
        data = table_construct(14, 7)
        for course in courses:
            data[course.daytime - 1][course.weekday - 1] = course.coursename
        return data


    def propost(request):
        data = request.body
        jdata = json.loads(data) #把post信息转化为json格式

        # 加入数据库
        if CourseModel.add_by_json(jdata):
            return HttpResponse(success())
        return HttpResponse(fail())

class Student(View):
    def add(request):
        # data = request.body.decode('utf-8')
        data = request.body
        jdata = json.loads(data)

        reason, status = StudentModel.add_student(jdata)
        if status:
            return HttpResponse(success(jdata))
        return HttpResponse(fail(reason))

    def login(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = StudentModel.login_confirm(jdata['stuid'], jdata['secret'])
        if status:
            return HttpResponse(success(reason))
        return HttpResponse(fail(reason))

class Affair(View):
    def set_affair(request):
        jdata = jsonify(request)
        reason, status = AffairModel.add_by_json(jdata)

        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(jdata))

    def get_affair(request):
        data = request.body
        jdata = json.loads(data)
        id = jdata["stuid"]
        week = jdata["currweek"]
        affairs = AffairModel.objects(stuid = id, weeknum = week)
        infos = []
        for affair in affairs:
            info = {
                'stuid':affair.stuid,
                'weeknum':affair.weeknum,
                'weekday':affair.weekday,
                'daytime':affair.daytime,
                'affair':affair.affairname
            }
            infos.append(info)
        
        if len(infos) == 0:
            return HttpResponse(fail({"reason":"No affairs"}))
        return HttpResponse(success({"data":infos}))        