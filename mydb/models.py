from django.db import models

# Create your models here.
import mongoengine
import json

class CourseModel(mongoengine.Document):
    stuid = mongoengine.StringField(max_length=12, required=True) #学生学号
    name = mongoengine.StringField(max_length=5) #学生姓名
    coursename = mongoengine.StringField(max_length=20) #课程名称
    weekday = mongoengine.IntField(min_value=0, max_value=7) #描述课程是一周中的那一天
    daytime = mongoengine.IntField(min_value=0, max_value=15) #描述课程在一天中的第几节


    def add_by_json(jdata):
        """
        把post的json数据转化，创建新的Course
        """
        stuid2add = jdata['stuid']
        name2add = jdata['name']
        course2add = jdata['course']
        week2add = jdata['weekday']
        day2add = jdata['daytime']

        student = StudentModel.objects(stuid = stuid2add).first()
        if not student:
            return {"reason":"找不到当前学生"}, False
        if student.name != name2add:
            return {"reason":"学生名字错误"}, False
        if week2add > 7:
            return {"reason":"日期错误"}, False
        if day2add > 14:
            return {"reason":"时间错误"}, False
        
        find_obj = CourseModel.objects(stuid = stuid2add, name = name2add, weekday = week2add, daytime = day2add).first()

        if not find_obj:
            course = CourseModel(stuid = stuid2add, name = name2add, coursename = course2add, weekday = week2add, daytime = day2add)
            course.save()
        else:
            find_obj.coursename = course2add
            if len(course2add) == 0:
                find_obj.delete()
            else:
                find_obj.save()

        return {"reason":"success"}, True

class StudentModel(mongoengine.Document):
    stuid = mongoengine.StringField(max_length=12, required=True, unique=True) #学生学号
    name = mongoengine.StringField(max_length=5) #学生姓名
    secret = mongoengine.StringField(max_length=16, min_length=6) #密码

    def add_student(jdata):
        stuid2add = jdata['stuid']
        name2add = jdata['name']
        secret2add = jdata['secret']

        data = StudentModel.objects(stuid = stuid2add)
        if len(data) > 0:
            return {"reason":"该学号已存在"}, False
        if len(stuid2add) != 11:
            return {"reason":"学号长度不正确"}, False
        if len(secret2add) < 6 or len(secret2add) > 16:
            return {"reason":"密码长度不合适"}, False
        
        student = StudentModel(stuid=stuid2add, name=name2add, secret=secret2add)
        student.save()

        return {"reason":"添加成功"}, True

    def login_confirm(id, password):
        stu = StudentModel.objects(stuid = id).first()
        if not stu:
            return {"reason":"找不到该帐号"}, False
        if stu.secret != password:
            return {"reason":"密码错误"}, False
        return {"name":stu.name, "id":id}, True

    def student_exist(sid):
        student = StudentModel.objects(stuid = sid).first()
        if not student:
            return False
        return True

class AffairModel(mongoengine.Document):
    stuid = mongoengine.StringField(max_length=12, required=True) #学生学号
    name = mongoengine.StringField(max_length=5) #学生姓名
    affairname = mongoengine.StringField(max_length=20) #事务名称
    weeknum = mongoengine.IntField(min_value=0, max_value=18) #描述事务位于第几周
    weekday = mongoengine.IntField(min_value=0, max_value=7) #描述事务是一周中的那一天
    daytime = mongoengine.IntField(min_value=0, max_value=14) #描述事务在一天中的第几节

    def add_by_json(jdata):
        stuid2add = jdata['stuid']
        name2add = jdata['name']
        affair2add = jdata['affair']
        week2add = jdata['weekday']
        day2add = jdata['daytime']
        weekcount = jdata['weeknum'] #周数

        student = StudentModel.objects(stuid = stuid2add).first()
        # 检验数据是否合理
        if not student:
            return {"reason":"找不到当前学生"}, False
        if student.name != name2add:
            return {"reason":"学生名字错误"}, False
        if week2add > 7:
            return {"reason":"日期错误"}, False
        if day2add > 14:
            return {"reason":"时间错误"}, False
        if weekcount > 18:
            return {"reason":"星期错误"}, False
        
        find_obj = AffairModel.objects(stuid = stuid2add, name = name2add, weekday = week2add, daytime = day2add, weeknum = weekcount).first()
        if not find_obj:
            affair = AffairModel(stuid = stuid2add, name = name2add, affairname = affair2add, weekday = week2add, daytime = day2add, weeknum = weekcount)
            affair.save()
        else:
            find_obj.affairname = affair2add
            if len(affair2add) == 0:
                find_obj.delete()
            else:
                find_obj.save()

        return {"reason":"success"}, True

class GroupModel(mongoengine.Document):
    groupid = mongoengine.StringField(required=True) # 小组编号
    groupname = mongoengine.StringField(max_length=20) # 小组名称
    leader = mongoengine.StringField(max_length=12) # 组长学号
    stuid = mongoengine.StringField(max_length=12) # 学生学号
    destroy = mongoengine.IntField() # 是否被摧毁，1为不可用，0为可用

    def create_group(jdata):
        gname2add = jdata["groupname"]
        stuid2add = jdata["stuid"]
        if not StudentModel.student_exist(stuid2add):
            return {"reason":"学生信息不存在"}, False
        if not gname2add:
            return {"reason":"小组名字不能为空"}, False
        elif len(gname2add) > 20:
            return {"reason":"小组名字太长了！"}, False
        nid = len(GroupModel.objects()) + 1
        nid = str(nid)
        group = GroupModel(groupid = nid, groupname = gname2add, leader = stuid2add, stuid = stuid2add, destroy = 0)
        group.save()
        return {"reason":"添加成功"}, True

    # 加入小组
    def join_group(jdata):
        gid2add = jdata["groupid"]
        stuid2add = jdata["stuid"]
        find_group = GroupModel.objects(groupid = gid2add, destroy = 0).first()
        if not find_group:
            return {"reason":"小组id不存在"}, False
        exist_stu = GroupModel.objects(groupid = gid2add, stuid = stuid2add, destroy = 0).first()
        if exist_stu:
            return {"reason":"已经加入小组"}, False
        join_stu = GroupModel(groupid = gid2add, groupname = find_group.groupname, leader = find_group.leader, stuid = stuid2add, destroy = 0)
        join_stu.save()
        return {"reason":"成功加入小组"}, True

    # 退出小组
    def leave_group(jdata):
        gid2del = jdata["groupid"]
        stuid2del = jdata["stuid"]
        find_item = GroupModel.objects(groupid = gid2del, stuid = stuid2del, destroy = 0)
        if len(find_item) == 0:
            return {"reason":"记录不存在"}, False
        for item in find_item:
            if item.leader == stuid2del:
                return {"reason":"组长不能退出小组"}, False
            item.delete()
        return {"reason":"删除成功"}, True

    # 更改组长
    def change_leader(jdata):
        gid2chg = jdata["groupid"]
        lid2chg = jdata["leaderid"]
        sid2chg = jdata["newleader"]
        if lid2chg == sid2chg:
            return {"reason":"没有实际更改"}, False
        change_items = GroupModel.objects(groupid = gid2chg, leader = lid2chg, destroy = 0)
        if len(change_items) == 0:
            return {"reason":"没有记录"}, False
        for item in change_items:
            item.leader = sid2chg
            item.save()
        return {"reason":"修改成功"}, True

    # 列出小组和组长名单
    def show_groups(jdata):
        sid2show = jdata["stuid"]
        group_list = GroupModel.objects(stuid = sid2show, destroy = 0)
        infos = []
        for item in group_list:
            info = {
                "groupid":item.groupid,
                "groupname":item.groupname,
                "leader":item.leader,
                "permission":(item.leader == sid2show)
            }
            infos.append(info)
        return infos

    def destroy_group(jdata):
        stuid2des = jdata["stuid"]
        group2des = jdata["groupid"]
        groups = GroupModel.objects(leader = stuid2des, groupid = group2des, destroy = 0)
        if len(groups) == 0:
            return {"reason":"没有权限解散或是小组不存在"}, False
        for item in groups:
            item.destroy = 1
            item.save()
        return {"reason":"摧毁成功"}, True

class GroupAffairModel(mongoengine.Document):
    groupid = mongoengine.StringField() # 小组编号
    affairname = mongoengine.StringField(max_length=20) # 事务名称
    weeknum = mongoengine.IntField(min_value=0, max_value=18) # 事务位于第几周
    weekday = mongoengine.IntField(min_value=0, max_value=7) # 周几
    daytime = mongoengine.IntField(min_value=0, max_value=14) # 第几节课

    # 添加小组事务
    def change_group_affair(jdata):
        aff2add = jdata["affair"]
        stuid = jdata["stuid"]
        gid2add = jdata["groupid"]
        weeknum2add = jdata["weeknum"]
        weekday2add = jdata["weekday"]
        daytime2add = jdata["daytime"]
        check_leader = GroupModel.objects(leader = stuid, groupid = gid2add, destroy = 0).first()
        if not check_leader:
            return {"reason":"不存在该小组-组长对"}, False
        old_affair = GroupAffairModel.objects(groupid = gid2add, weeknum = weeknum2add, weekday = weekday2add, daytime = daytime2add).first()
        if old_affair:
            if jdata["op"] == "add":
                old_affair.affairname = aff2add
                old_affair.save()
                return {"reason":"修改小组事务成功"}, True
            elif jdata["op"] == "delete":
                old_affair.delete()
                return {"reason":"删除小组事务成功"}, True
        if jdata["op"] == "delete":
            return {"reason":"小组事务不存在，删除失败"}, False
        if jdata["op"] != "add":
            return {"reason":"操作名不存在"}, False
        new_affair = GroupAffairModel(groupid = gid2add, affairname = aff2add, weeknum = weeknum2add, weekday = weekday2add, daytime = daytime2add)
        new_affair.save()
        return {"reason":"添加小组事务成功"}, True