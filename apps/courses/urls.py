from django.conf.urls import url
from apps.courses.views import CourseListView,CourseDetailView,CourseLessonView,CourseCommentsView,VideoView
urlpatterns = [
    #列表页
    url(r'^list/$',CourseListView.as_view(),name="list"),
    #详情页
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),
    #章节信息
    url(r'^(?P<course_id>\d+)/lesson/$', CourseLessonView.as_view(), name="lesson"),
    #评论
    url(r'^(?P<course_id>\d+)/comments/$', CourseCommentsView.as_view(), name="comments"),
    #视频
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', VideoView.as_view(), name="video"),

]