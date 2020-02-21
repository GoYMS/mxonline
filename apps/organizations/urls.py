from django.conf.urls import url

from apps.organizations.views import OrgView,AddAskView,OrgHomeView,OrgTeacherView,OrgCourseView,OrgDescView,TeachersView,TeacherDetailView
urlpatterns = [
    #列表页
    url(r'^list/$',OrgView.as_view(),name="list"),
    #列表右侧用户咨询
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    #机构首页
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    #机构讲师
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    #机构课程
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),
    #机构简介
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),


    #讲师页面
    #讲师列表页
    url(r'^teachers/$', TeachersView.as_view(), name="teachers"),
    #讲师详情页面
    url(r'^teachers/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name="teacher_detail"),

]