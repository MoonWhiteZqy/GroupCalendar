"""GroupCalendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from mydb.views import Course, Student, Affair, Group, GroupAffair

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.login), #登录页面
    url(r'^index/$', views.index), #课表页面
    url(r'^group/$', views.group), #团队页面
    url(r'^add/course/$', Course.add_course), #添加课程
    url(r'^get/$', Course.get_course), #获取课程
    url(r'^add/student/$', Student.add), #添加学生
    url(r'^login/$', Student.login), #用户登录
    url(r'^add/affair/$', Affair.set_affair), #添加事务
    url(r'^get/affair$', Affair.get_affair), #获取事务
    url(r'^group/join$', Group.join_group), #加入小组
    url(r'^group/create$', Group.create_group), #创建小组
    url(r'^group/leave$', Group.leave_group), #离开小组
    # url(r'^group/change$', Group.change_leader), #更改组长
    url(r'^group/show$', Group.show_group), #展示加入的小组
    url(r'^group/destroy$', Group.destroy_group), #组长解散自己的小组
    url(r'^group/affair/change$', GroupAffair.change_group_affair), #组长添加、删除小组事务
    url(r'^group/search$', Group.search_group), #根据组长学号查找小组
]
