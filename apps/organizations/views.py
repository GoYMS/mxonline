from django.shortcuts import render
from django.views.generic.base import View
from apps.organizations.models import CourseOrg,City,Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from apps.organizations.forms import AddAskForm
from django.http import JsonResponse
from apps.operations.models import UserFavorite
from django.db.models import Q


#列表页右侧的用户提交的信息
#注意这个表单的信息的验证等工作还是放在forms中进行
class AddAskView(View):
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)  #commit=True这个必须要有，save只是提交到数据库，加上这个才会保存
            #此处还应该修改参照前端中的js
            return JsonResponse({
                "status":"success"
            })

        else:
            return JsonResponse({
                "status": "fail",
                "msg":"提交出错！请检查格式！",
            })


#讲师列表页
class TeachersView(View):
    def get(self, request, *args, **kwargs):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        # 全局搜索功能
        keywords = request.GET.get("keywords", "")
        s_type = 'teacher'
        if keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=keywords))

        #人气排行
        sort = request.GET.get("sort","")
        if sort:

            all_teachers = all_teachers.order_by('-click_nums')

        #讲师排行榜
        hot_teachers =  all_teachers.order_by('-click_nums')[:2]

        # 对讲师列表数据的分页
        try:
            page = request.GET.get('page', 1)   #这里边的page是前端页面中分页代码中的页面路径中的参数，要与之对应
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, per_page=3, request=request)  # per_page一页显示几个数据
        teachers = p.page(page)
        current_page = "teacher"
        return render(request,'teachers-list.html',{
            "teachers":teachers,
            "teacher_nums":teacher_nums,
            "current_page":current_page,
            "sort":sort,
            "hot_teachers":hot_teachers,
            "keywords": keywords,
            "s_type": s_type

        })
#讲师详情页
class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        #讲师信息
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        #讲师的所属机构
        org = teacher.org
        #讲师的课程
        teacher_courses = teacher.course_set.all()
        # 讲师排行榜
        teachers = Teacher.objects.all()
        hot_teachers = teachers.order_by('-click_nums')[:2]
        current_page = 'teacher'
        #搜索中使用
        s_type="teacher"

        #收藏
        teacher_fav = False
        org_fav =False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_type=3,fav_id=teacher.id):
                teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True
        return render(request,"teacher-detail.html",{
            "teacher":teacher,
            "teacher_courses":teacher_courses,
            "hot_teachers":hot_teachers,
            "org":org,
            "teacher_fav":teacher_fav,
            "org_fav":org_fav,
            "current_page":current_page,
            "s_type":s_type
        })



#列表页的排序
class OrgView(View):
    def get(self, request, *args, **kwargs):
        #得到后台的数据
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()

        # 全局搜索功能
        keywords = request.GET.get("keywords", "")
        s_type = 'org'
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        #右侧对授课机构进行排序
        hot_orgs = all_orgs.order_by("-click_nums")[:3]  #进行切片，选取三个

        #通过机构类别对课程机构的筛选
        category = request.GET.get("ct","")
        if category:
            all_orgs = all_orgs.filter(category=category)


        #通过所在城市对课程机构进行筛选
        city_id = request.GET.get("city","")
        if city_id:
            if city_id.isdigit(): #isdigit() 检测字符串是否只由数字组成。
                all_orgs = all_orgs.filter(city_id=int(city_id))
        #对课程机构进行排序
        sort = request.GET.get('sort','')
        if sort == 'students':
            #按照学习人数进行排序
            all_orgs = all_orgs.order_by("-students")
        elif sort == 'courses':
            #按照课程人数进行排序
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        # 对课程机构数据的分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=5,request=request) #per_page一页显示几个数据
        orgs = p.page(page)
        org = "organizations"
        return render(request,'org-list.html',{
            "all_orgs":orgs,
            "org_nums":org_nums,
            "all_citys":all_citys,
            "category":category,
            "city_id":city_id,
            "sort":sort,
            "hot_orgs":hot_orgs,
            "current_page":org,
            "keywords": keywords,
            "s_type": s_type


        })

#机构首页
class OrgHomeView(View):
    def get(self, request, org_id,*args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))

        #点击数增加
        course_org.click_nums +=1
        course_org.save()
        #课程数
        all_courses = course_org.course_set.all()[:3]  #_set.all  课程信息不在培训机构中，使用这种方法可以得到机构对应的课程信息
        #教师
        all_teacher = course_org.teacher_set.all()[:1]

        #收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True


        current_page = "home"
        return render(request,'org-detail-homepage.html',{
            "all_courses":all_courses,
            "all_teacher":all_teacher,
            "course_org":course_org,
            "current_page": current_page,
            "has_fav":has_fav
        })
#机构讲师
class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 点击数增加
        course_org.click_nums += 1
        course_org.save()
        #获得讲师信息
        all_teacher = course_org.teacher_set.all()
        # 收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        current_page = 'teacher'
        return render(request,'org-detail-teachers.html',{
                    "all_teacher":all_teacher,
                    "course_org":course_org,
                    "current_page": current_page,
            "has_fav":has_fav,
                })
#机构课程
class  OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 点击数增加
        course_org.click_nums += 1
        course_org.save()
        #获得课程信息
        all_courses = course_org.course_set.all()

        # 对机构课程的数据的分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=5, request=request)  # per_page一页显示几个数据
        courses = p.page(page)  #此处courses不是列表的形式了
        # 收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        current_page = 'course'
        return render(request,'org-detail-course.html',{
                    "all_courses":courses,
                    "course_org":course_org,
                    "current_page": current_page,
            "has_fav":has_fav
                })
#机构介绍
class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 点击数增加
        course_org.click_nums += 1
        course_org.save()
        # 收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        current_page = 'desc'
        return render(request, 'org-detail-desc.html', {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav":has_fav,
        })
