from apps.users.models import BaseModel
from apps.organizations.models import Teacher

from django.db import models

from apps.organizations.models import CourseOrg
from DjangoUeditor.models import UEditorField
from datetime import datetime
"""
数据表的设计思想
实体1 《关系》 实体2
也就是将关于课程相关的所有信息，分为几种实体，例如，课程详情页的所有信息为一个实体，
在课程章节中所有的信息设计为一个实体,

"""


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name="讲师")
    course_org = models.ForeignKey(CourseOrg,null=True,blank=True,on_delete=models.CASCADE,verbose_name="课程机构")
    name = models.CharField(verbose_name="课程名",max_length=50)
    desc = models.CharField(verbose_name="课程描述",max_length=300)
    learn_times = models.IntegerField(default=0,verbose_name="学习时长")
    degree = models.CharField(verbose_name="难度",choices=(("cj","初级"),("zj","中级"),("gj","高级")),max_length=2)
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    notice = models.CharField(default='',verbose_name="课程公告",max_length=200)
    category = models.CharField(default="后端开发",max_length=20,verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    youneed_know = models.CharField(default="", max_length=300,verbose_name="课程须知")
    teacher_tell = models.CharField(default="",max_length=300,verbose_name="老师告诉你")
    detail = UEditorField(verbose_name="课程详情",width=600,height=300,imagePath="course/ueditor/images/",
                               filePath="course/ueditor/files/",default="")
    image = models.ImageField(upload_to="courses/%Y/%m",verbose_name="封面图",max_length=100)
    is_classics = models.BooleanField(default=False,verbose_name="是否经典内容")
    is_banner = models.BooleanField(default=False,verbose_name="是否广告位")

    #verbose_name指定在admin管理界面中显示中文；verbose_name表示单数形式的显示，
    # verbose_name_plural表示复数形式的显示；中文的单数和复数一般不作区别。

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()


#自定义方法在xadmin列表中显示所需要的东西

    #显示课程的封面图
    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}'>".format(self.image.url))
    show_image.short_description = '封面图片'  #这个是在后台中显示列表的名称是什么
#最后记得需要将方法名称写入adminx中
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/{}'>跳转</a>".format(self.id))

    go_to.short_description = '跳转'  # 这个是在后台中显示列表的名称是什么
    # 最后记得需要将方法名称写入adminx中


class Lesson(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")#on_delete表示对应的外键数据被删除后，当前的数据应该也删除
    name = models.CharField(max_length=100,verbose_name="章节名")
    learn_times = models.IntegerField(default=0,verbose_name="学习时长(分钟)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



class Video(BaseModel):

    lesson = models.ForeignKey(Lesson,verbose_name="章节",on_delete=models.CASCADE)
    name = models.CharField(max_length=100,verbose_name="视频名称")
    learn_time = models.IntegerField(default=0,verbose_name="学习时长(分钟)")
    url = models.CharField(max_length=1000,verbose_name="访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(BaseModel):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="课程")
    name = models.CharField(max_length=100,verbose_name="名称")
    download = models.FileField(upload_to="course/resourse/%Y/%m",verbose_name="下载地址",max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name