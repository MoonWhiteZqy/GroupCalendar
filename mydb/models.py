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
        course2add = jdata['coursename']
        week2add = jdata['weekday']
        day2add = jdata['daytime']

        student = StudentModel.objects(stuid = stuid2add).first()
        if not student:
            return False
        if student.name != name2add:
            return False
        
        course = CourseModel(stuid = stuid2add, name = name2add, coursename = course2add, weekday = week2add, daytime = day2add)
        course.save()

        return True

class StudentModel(mongoengine.Document):
    stuid = mongoengine.StringField(max_length=12, required=True, unique=True) #学生学号
    name = mongoengine.StringField(max_length=5) #学生姓名
    secret = mongoengine.StringField(max_length=16, min_length=6) #密码
    gender = mongoengine.StringField(max_length=1, min_length=1) #性别

    def add_student(jdata):
        stuid2add = jdata['stuid']
        name2add = jdata['name']
        secret2add = jdata['secret']
        gender2add = jdata['gender']

        student = StudentModel(stuid=stuid2add, name=name2add, secret=secret2add, gender = gender2add)
        student.save()

        return True

    def login_confirm(id, password):
        stu = StudentModel.objects(stuid = id).first()
        if not stu:
            return "id doesn't exist", False
        if stu.secret != password:
            return "password is wrong", False
        return "login confirmed", True

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
            return "ID not found", False
        if student.name != name2add:
            return "Not this student", False
        if week2add > 7:
            return "No this day", False
        if day2add > 14:
            return "No this class time", False
        if weekcount > 18:
            return "No this week", False
        
        affair = AffairModel(stuid = stuid2add, name = name2add, affairname = affair2add, weekday = week2add, daytime = day2add, weeknum = weekcount)
        affair.save()

        return "success", True