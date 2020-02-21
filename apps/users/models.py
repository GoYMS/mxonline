from django.db import models
from django.utils import timezone
from datetime import datetime

#此处讲的是覆盖掉了原来就有的一个user表

from  django.contrib.auth.models import AbstractUser


def unread_nums(request):
    # 未读消息数量
    if request.user.is_authenticated:
        return {'unread_nums':request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}

#此处为公用的一个模板类，用来记录课程中创建的时间，写在此处是因为user表与其他的几个没有
#相互冲突，属于最底层的一个模板，
class BaseModel(models.Model):
    datetime = models.DateTimeField(default=timezone.now,verbose_name="创建的时间")

    class Meta:
       abstract = True  #在进行数据迁移的时候，这个类不再进行表的创建



#用于下面的性别
GENDER_CHOICES = (
    ("male",'男'),
    ("female",'女'),
)

#继承的是django本身就有的一个类
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name="昵称",default="")
    birthday = models.DateField(verbose_name="生日",null=True,blank=True)
    gender = models.CharField(verbose_name="性别",choices=GENDER_CHOICES,max_length=6)
    address = models.CharField(max_length=100,verbose_name="地址",default="")
    mobile = models.CharField(max_length=11,verbose_name="手机号码")
    image = models.ImageField(upload_to="head_image/%Y/%m",default="default.jpg",verbose_name="用户头像")
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name


    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username