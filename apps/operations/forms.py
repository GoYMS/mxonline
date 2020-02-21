from django import forms
from apps.operations.models import UserFavorite,CourseComments


#此处使用的是相当于继承model中的各种变量数据
class UserFavForm(forms.ModelForm):

    class Meta:
        model = UserFavorite
        fields = ["fav_id","fav_type"]

class CommentForm(forms.ModelForm):

    class Meta:
        model = CourseComments
        fields = ["comments","course"]
