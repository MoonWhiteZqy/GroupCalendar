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