import xadmin

from apps.operations.models import UserAsk,CourseComments,UserCourse,UserFavorite,UserMessage,Banner


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'datetime','index']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url', 'datetime','index']

class UserAskAdmin(object):


    list_display = ['title', 'image', 'url','index']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'datetime']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'datetime']

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read','datetime']
    search_fields = ['user','message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'datetime']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course','comments', 'datetime']
    search_fields = ['user', 'course','comments']
    list_filter = ['user', 'course', 'comments','datetime']

class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'datetime']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'datetime']


xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)
xadmin.site.register(UserFavorite,UserFavoriteAdmin)