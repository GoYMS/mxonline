from django import forms
from captcha.fields import CaptchaField
import redis
from MxOnline.settings import REDIS_PORT,REDIS_HOST
from apps.users.models import UserProfile

#修改手机号
class UpdateMobileForm(forms.Form):
    mobile = forms.CharField(required=True,min_length=11,max_length=11)
    code = forms.CharField(required=True,min_length=4,max_length=4)

    #手机发送的验证码是否正确
    def clean_code(self):
        #取值
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            #传出错误消息
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data



#修改密码
#由于在model中没有密码这个，所以直接在form中写
class ChangePwdForm(forms.Form):   # 变量名要与前端的中一样
    password1 = forms.CharField(required=True,min_length=6,max_length=11)
    password2 = forms.CharField(required=True, min_length=6, max_length=11)



#处理用户上传的头像
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


#处理用户信息的修改
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name","birthday","gender","address"]  #这里对应的值要与model中和前端js（data.xxx）中的一样


class LoginForm(forms.Form):
    #前边的变量名需要与前端页面的input中的name属性的值相同
    username = forms.CharField(required=True,min_length=2)
    password = forms.CharField(required=True,min_length=3)


#图片动态验证码
class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True,min_length=11,max_length=11)
    captcha = CaptchaField()


#登录页面验证手机号和验证码
class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True,min_length=11,max_length=11)
    code = forms.CharField(required=True,min_length=4,max_length=4)

    #验证码是否正确
    def clean_code(self):
        #取值
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            #传出错误消息
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data

#注册页面
class RegisterGetForm(forms.Form):
    captcha = CaptchaField()

class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        # 验证手机号码是否已经注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("该手机号已经注册")
        return mobile
    # 验证码是否正确
    def clean_code(self):
        # 取值
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            # 传出错误消息
            raise forms.ValidationError("验证码不正确")
        return code