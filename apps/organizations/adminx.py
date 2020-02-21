import xadmin

from apps.organizations.models import Teacher,CourseOrg,City

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CourseOrgAdmin(object):
    list_display = ['name','desc','click_nums','fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']


class CityAdmin(object):
    #显示一条数据的哪几个内容
    list_display = ["id","name","desc"]
    #以那几条数据进行查询
    search_fields = ["name","desc"]
    #过滤器
    list_filter = ["name","desc","datetime"]
    #那几条数据可以直接进行修改
    list_editable = ["name","desc"]

xadmin.site.register(Teacher,TeacherAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(City,CityAdmin)