from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect, reverse

# Create your views here.
from .models import CourseModel, StudentModel, AffairModel, GroupModel, GroupAffairModel
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


    def add_course(request):
        data = request.body
        jdata = json.loads(data) #把post信息转化为json格式

        # 加入数据库
        reason, status = CourseModel.add_by_json(jdata)
        if status:
            return HttpResponse(success(jdata))
        return HttpResponse(fail(reason))

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
        groups = GroupModel.objects(stuid = id, destroy = 0)
        ginfos = [] # 记录当前用户所在小组的事务
        for group in groups:
            gid = group.groupid
            group_affairs = GroupAffairModel.objects(groupid = gid, weeknum = week)
            for affair in group_affairs:
                info = {
                    'stuid':id,
                    'weeknum':week,
                    'weekday':affair.weekday,
                    'daytime':affair.daytime,
                    'affair':affair.affairname
                }
                ginfos.append(info)
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
        return HttpResponse(success({"data":infos, "gdata":ginfos}))
        
    def delete_affair(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = AffairModel.delete_all(jdata)
        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(reason))

class Group(View):
    def create_group(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = GroupModel.create_group(jdata)
        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(jdata))

    def join_group(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = GroupModel.join_group(jdata)
        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(jdata))

    def leave_group(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = GroupModel.leave_group(jdata)
        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(reason))

    def change_leader(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = GroupModel.change_leader(jdata)
        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(reason))

    def show_group(request):
        data = request.body
        jdata = json.loads(data)
        reslist = GroupModel.show_groups(jdata)
        return HttpResponse(json.dumps({"data":reslist}))

    def destroy_group(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = GroupModel.destroy_group(jdata)
        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(reason))

    def search_group(request):
        data = request.body
        jdata = json.loads(data)
        hisgroups = GroupModel.search_group(jdata)
        res = []
        for group in hisgroups:
            gdata = {
                "groupid":group.groupid,
                "groupname":group.groupname
            }
            res.append(gdata)
        status = {
            "len":len(res),
            "data":res
        }
        return HttpResponse(success(status))

class GroupAffair(View):
    def change_group_affair(request):
        data = request.body
        jdata = json.loads(data)
        reason, status = GroupAffairModel.change_group_affair(jdata)
        if not status:
            return HttpResponse(fail(reason))
        return HttpResponse(success(reason))

    def table_get_affair(request):
        jdata = json.loads(request.body)
        gid = jdata["groupid"]
        wknum = jdata["weeknum"]
        affairs = GroupAffairModel.objects(groupid = gid, weeknum = wknum)
        individuals = GroupModel.objects(groupid = gid)
        group_data = table_construct(14, 7)
        individual_data = table_construct(14, 7)
        for affair in affairs:
            group_data[affair.daytime - 1][affair.weekday - 1] = affair.affairname
        for individual in individuals:
            student = individual.stuid
            stu_affair = AffairModel.objects(stuid = student, weeknum = wknum)
            for single_affair in stu_affair:
                individual_data[single_affair.daytime - 1][single_affair.weekday - 1] = single_affair.name
        data = {
            'group':group_data,
            'individual':individual_data
        }
        return HttpResponse(success(data))