from django.shortcuts import render
from django.views.generic import View
from apps.operations.models import UserFavorite,CourseComments,Banner
from apps.operations.forms import UserFavForm,CommentForm
from apps.courses.models import Course
from apps.organizations.models import CourseOrg,Teacher
from django.http import JsonResponse


# Create your views here.
#收藏按钮在这里



#首页
class IndexView(View):
    def get(self, request, *args, **kwargs):
        #最大轮播图
        banners = Banner.objects.all().order_by("index")
        #不展示出来的课程
        courses = Course.objects.all()
        #展示出来的课程
        banner_courses = Course.objects.filter(is_banner=True)
        #课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        s_type = ''

        return render(request,"index.html",{
            "banners":banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs,
            "s_type":s_type

        })


class AddFavView(View):
    def post(self, request,  *args, **kwargs):
        """
        用户收藏，取消收藏
        """
        #用户收藏之前需要判断是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status":"fail",
                "msg":"用户未登录"
            })
        user_fav_form  = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            #是否已经收藏
            existed_records = UserFavorite.objects.filter(user=request.user,fav_id=fav_id,fav_type=fav_type)
            #如果已经收藏，再点击说明是要取消收藏
            if existed_records:
                existed_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id = fav_id)
                    course.fav_nums -=1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    "status":"success",
                    "msg":"未收藏"

                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                if fav_type == 1:
                    course = Course.objects.get(id = fav_id)
                    course.fav_nums +=1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums += 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏",
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "收藏失败",
            })


#用户评论
class CommentView(View):
    def post(self, request,  *args, **kwargs):

        #用户评论之前需要判断是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status":"fail",
                "msg":"用户未登录"
            })
        comment_form  = CommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments

            comment.course = course
            comment.save()

            return JsonResponse({
                "status": "success",

            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "评论失败",
            })



