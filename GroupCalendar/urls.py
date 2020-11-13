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
from mydb.views import Course, Student, Affair

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', views.login),
    url(r'^index/$', views.index),
    url(r'^add/$', Course.propost), #添加课程
    url(r'^get/$', Course.get_course), #获取课程
    url(r'^add/student/$', Student.add), #添加学生
    url(r'^login/$', Student.login), #用户登录
    url(r'^add/affair/$', Affair.set_affair), #添加事务
    url(r'^get/affair$', Affair.get_affair), #获取事务
]
