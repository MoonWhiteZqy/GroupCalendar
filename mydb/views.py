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

    def default_affair(request):
        data = request.body
        jdata = json.loads(data)
        # 下午课程要+1， 晚上课程要+2
        default_course = {
                "工程伦理":[
                    {"from":10, "to":19, "weekday":4, "up":7, "down":10}],
                "研究生综合英语":[
                    {"from":2, "to":2, "weekday":1, "up":1, "down":4},
                    {"from":4, "to":5, "weekday":1, "up":1, "down":4},
                    {"from":6, "to":6, "weekday":6, "up":1, "down":4},
                    {"from":7, "to":12, "weekday":1, "up":1, "down":4},
                    ],
                "算法设计与分析":[
                    {"from":2, "to":5, "weekday":2, "up":1, "down":2},
                    #{"from":9, "to":11, "weekday":3, "up":11, "down":11},
                    #{"from":13, "to":15, "weekday":3, "up":11, "down":11},
                    #{"from":17, "to":17, "weekday":3, "up":11, "down":11},
                    #{"from":19, "to":19, "weekday":3, "up":11, "down":11},
                    {"from":2, "to":5, "weekday":4, "up":3, "down":5},
                    {"from":7, "to":19, "weekday":4, "up":3, "down":5},
                    ],
                "高级软件工程":[
                    {"from":9, "to":10, "weekday":3, "up":3, "down":5},
                    {"from":2, "to":5, "weekday":5, "up":7, "down":9},
                    {"from":6, "to":6, "weekday":7, "up":7, "down":9},
                    {"from":7, "to":18, "weekday":5, "up":7, "down":9},
                    ],
                "软件体系结构":[
                    {"from":2, "to":5, "weekday":2, "up":7, "down":9},
                    {"from":7, "to":13, "weekday":2, "up":7, "down":9},
                    #{"from":7, "to":14, "weekday":2, "up":11, "down":11},
                    {"from":2, "to":5, "weekday":5, "up":1, "down":2},
                    {"from":6, "to":6, "weekday":7, "up":1, "down":2},
                    {"from":7, "to":13, "weekday":5, "up":1, "down":2},
                    ],
                "高级网络技术":[
                    {"from":2, "to":5, "weekday":2, "up":3, "down":5},
                    {"from":7, "to":18, "weekday":2, "up":3, "down":5},
                    #{"from":13, "to":17, "weekday":5, "up":11, "down":11},
                    ],
                "数据仓库与数据挖掘":[
                    {"from":2, "to":2, "weekday":1, "up":13, "down":14},
                    {"from":4, "to":5, "weekday":1, "up":13, "down":14},
                    {"from":6, "to":6, "weekday":6, "up":13, "down":14},
                    {"from":7, "to":12, "weekday":1, "up":13, "down":14},
                    {"from":2, "to":5, "weekday":3, "up":1, "down":2},
                    {"from":7, "to":12, "weekday":3, "up":1, "down":2},
                    #{"from":7, "to":11, "weekday":4, "up":11, "down":11},
                    ],
                "人工智能":[
                    #{"from":12, "to":16, "weekday":4, "up":11, "down":11},
                    {"from":2, "to":5, "weekday":5, "up":3, "down":5},
                    {"from":6, "to":6, "weekday":7, "up":3, "down":5},
                    {"from":7, "to":17, "weekday":5, "up":3, "down":5},
                    ],
                "区块链技术":[
                    {"from":2, "to":5, "weekday":3, "up":7, "down":10},
                    {"from":7, "to":12, "weekday":3, "up":7, "down":10},
                    ],
                "C++面向对象技术":[
                    {"from":2, "to":2, "weekday":1, "up":7, "down":9},
                    {"from":4, "to":5, "weekday":1, "up":7, "down":9},
                    {"from":6, "to":6, "weekday":6, "up":7, "down":9},
                    {"from":7, "to":9, "weekday":1, "up":7, "down":9},
                    {"from":2, "to":5, "weekday":3, "up":3, "down":5},
                    {"from":7, "to":8, "weekday":3, "up":3, "down":5},
                    ],
                "深度学习实践":[
                    {"from":11, "to":16, "weekday":1, "up":7, "down":9},
                    {"from":11, "to":17, "weekday":3, "up":3, "down":5},
                    ],
                "工程实验综合":[
                    ]
        }
        stuid = jdata["stuid"]
        course = jdata["default_course"]
        reason, status = AffairModel.many_affair(stuid, default_course[course], course)
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
