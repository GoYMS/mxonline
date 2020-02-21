import xadmin

from apps.courses.models import Course,Lesson,Video,CourseResource  #CourseTag


from xadmin.layout import Fieldset, Main, Side, Row, FormHelper

#修改左上角和页脚
class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"


#主题

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class CourseAdmin(object):
    list_display = ['name','desc','detail','degree','learn_times','students']
    search_fields = ['name','desc','detail','degree','students']
    list_filter = ['name','desc','detail','degree','learn_times','students']
    list_editable = ['degree','desc']




#怎样修改xadmin中的样式
class NewCourseAdmin(object):
    list_display = ['name','show_image', 'go_to','desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ['degree', 'desc']

    #这一列表示的是不能修改的数据,只读
    readonly_fields = ['click_nums','students','fav_nums']
    #隐藏某些字段
    exclude = ["datetime"]
    # 列表的按什么排序
    ordering = ['click_nums']
    #名字前边的小图标的样式设置
    model_icon = "fa fa-user"
    #富文本编辑相关配置
    style_fields = {
        "detail": "ueditor"
    }


   #数据过滤
    # 对应的讲师进入后台只能看到自己的课程
    #重载这个方法，就是显示返回那些数据
    def queryset(self):
        qs = super().queryset()   #所有课程
        if not self.request.user.is_superuser:  #判断是不是超级用户
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

#修改界面样式的方法
    def get_form_layout(self):
        #  if self.org_obj 加上这个的话是 在添加新的课程信息的界面还是原来的样子，但在查看课程页面的新的样式，如果删除，在添加或查看界面都是新的的样式
        if self.org_obj:
            self.form_layout = (
                #main是正中间的一个块
                Main(
                    Fieldset('讲师信息',
                             'teacher', 'course_org',
                             css_class='unsort no_title'  #区块不可以拖动
                             ),
                    Fieldset('基本信息',
                             'name', 'desc',
                             Row("learn_times","degree"),  #Row 是将括号中的放在一行
                             Row("category", "tag"),
                             "youneed_know","teacher_tell","detail"

                             ),
                     ),
                #Side是放在旁边的一个块
                Side(
                    Fieldset("访问信息",
                             "students","fav_nums","click_nums"
                    ),
                )
            )
            #最后这个记得要返回
        return super(NewCourseAdmin, self).get_form_layout()





class LessonAdmin(object):
    list_display = ['course','name','datetime']
    search_fields = ['course','name']
    list_filter = ['course__name','name','datetime']


class VideoAdmin(object):
    list_display = ['lesson','name','datetime']
    search_fields = ['lesson','name']
    list_filter = ['lesson','name','datetime']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download','datetime']
    search_fields = ['course', 'download','name']
    list_filter = ['course', 'name', 'download','datetime']
# class CourseTagAdmin(object):
#     list_display = ['course', 'tag',  'datetime']
#     search_fields = ['course', 'tag']
#     list_filter = ['course', 'tag', 'datetime']


xadmin.site.register(Course,NewCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView,BaseSettings)
# xadmin.site.register(CourseTag,CourseTagAdmin)
