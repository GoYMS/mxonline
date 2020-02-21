from django.conf.urls import url
from .views import MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView
from .views import UserImageView,UserInfoView,ChangePwdView
urlpatterns = [
    #个人信息
    url(r'^info/$',UserInfoView.as_view(),name="info"),
    #修改用户头像
    url(r'^image/upload/$',UserImageView.as_view(),name="image"),
    #修改密码
    url(r'^update/pwd/$',ChangePwdView.as_view(),name="pwd"),
    #修改手机号
    url(r'^update/mobile/$',ChangePwdView.as_view(),name="mobile"),
    #我的课程
    url(r'^mycourse/$',MyCourseView.as_view(),name="mycourse"),
    #我的收藏课程机构
    url (r'^myfavorg',MyFavOrgView.as_view(),name="myfavorg"),
    # 我的收藏课程教师
    url(r'^myfavteacher', MyFavTeacherView.as_view(), name="myfavteacher"),
    # 我的收藏课程
    url(r'^myfavcourse', MyFavCourseView.as_view(), name="myfavcourse"),
    #我的消息
    url(r'^message', MyMessageView.as_view(), name="message"),


]









