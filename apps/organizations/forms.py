from django import forms
from apps.operations.models import UserAsk
import re

#此处使用的是相当于继承model中的各种变量数据
class AddAskForm(forms.ModelForm):
    # 因为手机号为11位。但是在model中手机号没有进行最小最大设置，所以在这重新再设置一次
    mobile = forms.CharField(min_length=11,max_length=11,required=True)
    class Meta:
        model = UserAsk
        fields = ["name","mobile","course_name"]
    def clean_mobile(self):
        """
        验证手机号码是否格式正确
        """
        mobile = self.cleaned_data["mobile"]
        regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$" #验证手机号的正则表达式
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号非法",code="mobile_invalid")
