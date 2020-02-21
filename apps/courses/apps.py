from django.apps import AppConfig


class CoursesConfig(AppConfig):
    name = 'apps.courses'
    #此处设置是在后台中显示
    verbose_name = "课程管理"
 #写完之后在setting中也要添加