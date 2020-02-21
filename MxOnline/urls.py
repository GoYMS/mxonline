"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url,include
#使用新的一种方法
from django.views.generic import TemplateView
from apps.users.views import LoginView,LogoutView,SendSmsView,DynamicLoginView,RegisterView
import apps.organizations.urls as org #课程机构
import apps.operations.urls as op #用户操作
import apps.courses.urls as course #课程
import apps.users.urls as users
#上传图片，静态文件的处理方法
from django.views.static import serve
from MxOnline.settings import MEDIA_ROOT
#去除csrf的验证
from django.views.decorators.csrf import csrf_exempt
from apps.operations.views import IndexView
import xadmin
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    #此处使用的是django自带的方法，不通过views中的函数转到页面，而是直接转到相应的页面
    path('',IndexView.as_view(),name="index"), #首页
    path('login/',LoginView.as_view(),name="login"),  #登录页
    path('logout/',LogoutView.as_view(),name="logout"),  #退出
    url(r'^captcha/',include('captcha.urls')), #图片动态验证码
    #手机验证码，此处的名词必须与login.js中的一样,csrf_exempt去除相应函数的csrf的验证
    url(r'^send_sms/',csrf_exempt(SendSmsView.as_view()),name="send_sms"),
    path('d_login/', csrf_exempt(DynamicLoginView.as_view()), name="d_login"),  # 动态登录
    path('register/',RegisterView.as_view(),name="register"),

    #如果不写这个在后台管理系统中找不到图片，就是显示一个残图
    #serve,处理静态文件的方法，其参数需要知道前边path的路径以及后边在哪个路径下边
    url(r'^media/(?P<path>.*)/$',serve,{"document_root":MEDIA_ROOT}),
    #url(r'^static/(?P<path>.*)/$',serve,{"document_root":STATIC_ROOT}),


    #机构相关页面
    url(r'^org/',include((org,'organizations'),namespace="org")),
    # 课程相关页面
    url(r'^course/',include((course,'courses'), namespace="course")),
    #用户相关操作
    url(r'^op/',include((op,'operations'),namespace="op")),
    #用户个人中心
    url(r'^users/',include((users,'users'),namespace="users")),
    #富文本的相关url
    url(r'^ueditor/',include('DjangoUeditor.urls')),

]
