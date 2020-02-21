from django.shortcuts import render
from django.views.generic.base import View
from apps.courses.models import Course,CourseResource,Video
#分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.operations.models import UserFavorite,UserCourse,CourseComments
#装饰器
from django.contrib.auth.mixins import LoginRequiredMixin
#搜索中使用
from django.db.models import Q

#列表页
class CourseListView(View):
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.order_by("-datetime")
        #热门课程
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        # 全局搜索功能
        keywords = request.GET.get("keywords", "")
        s_type = 'course'
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(detail__icontains=keywords))


        #课程排序
        sort = request.GET.get("sort",'')
        if sort =='hot':
            all_courses = all_courses.order_by("-click_nums")
        elif sort == 'students':
            all_courses = all_courses.order_by("-students")


        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=3, request=request)  # per_page一页显示几个数据
        courses= p.page(page)


        course = "courses"
        return render(request,"course-list.html",{
            "all_courses":courses,
            "current_page":course,
            "sort":sort,
            "hot_courses":hot_courses,
            "keywords":keywords,
            "s_type":s_type
        })

#详情页
class CourseDetailView(View):
    def get(self, request,course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums +=1
        course.save()

        #搜索
        s_type = "course"



        #收藏
        has_fav_course = False
        has_fav_org=False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_id,fav_type=1):
                has_fav_course =True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=2):
                has_fav_org =True

        current_page = 'courses'
    #通过课程的tag做课程的推荐
        tag = course.tag
        related_courses = []
        if tag:                                             #排除这个主要的课程
            related_courses =Course.objects.filter(tag=tag).exclude(id=course.id)[:3]
        return render(request,'course-detail.html',{
            "course":course,
            "has_fav_course":has_fav_course,
            "has_fav_org":has_fav_org,
            "related_courses":related_courses,
            "current_page":current_page,
            "s_type":s_type
        })

#章节信息


class CourseLessonView(LoginRequiredMixin,View):
    #未登录跳转登录页面
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        """
        1.用户和课程之间的相关
        2.对view进行login登录验证
        3.其他课程
        """
        #查询用户是否已经关联这个课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
            course.students += 1
            course.save()
        #学过该课程的同学还学过
        user_courses =UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:3]
        related_courses =[]
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources =CourseResource.objects.filter(course=course)

        return render(request,"course-video.html",{
            "course":course,
            "course_resources":course_resources,
            "related_courses":related_courses
        })

#评论


class CourseCommentsView(LoginRequiredMixin,View):
    #未登录跳转登录页面
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        """
        1.用户和课程之间的相关
        2.对view进行login登录验证
        3.其他课程
        """
        #查询用户是否已经关联这个课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()
            course.students += 1
            course.save()
        #学过该课程的同学还学过
        user_courses =UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:3]
        related_courses =[]
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)


        #评论
        comments = CourseComments.objects.filter(course=course)
        #课程资源
        course_resources =CourseResource.objects.filter(course=course)

        return render(request,"course-comment.html",{
            "course":course,
            "course_resources":course_resources,
            "related_courses":related_courses,
            "comments":comments
        })
    #视频播放
class  VideoView(LoginRequiredMixin,View):
    # 未登录跳转登录页面
    login_url = "/login/"

    def get(self, request, course_id,video_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()


        video = Video.objects.get(id=int(video_id))

        # 查询用户是否已经关联这个课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        # 学过该课程的同学还学过
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:3]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        # 评论
        comments = CourseComments.objects.filter(course=course)
        # 课程资源
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "comments": comments,
            "video":video
        })





