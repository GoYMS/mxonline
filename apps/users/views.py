from django.shortcuts import render

#继承使用django内部的一个基于登录的方法
from django.views.generic.base import View

#django自带的一个验证登陆的方法
from django.contrib.auth import authenticate,login,logout

from django.http import HttpResponseRedirect,JsonResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
#直接使用url中的name，不用再写页面的名字
from django.urls import reverse
#使用form表单对登录验证
from apps.users.forms import LoginForm,DynamicLoginForm,DynamicLoginPostForm
from apps.users.forms import RegisterGetForm,RegisterPostForm,UploadImageForm,UserInfoForm,ChangePwdForm,UpdateMobileForm
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from apps.users.models import UserProfile
from MxOnline.settings import yp_apikey,REDIS_HOST,REDIS_PORT
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.operations.models import UserCourse,UserFavorite,UserMessage
from apps.organizations.models import CourseOrg,Teacher
from apps.courses.models import Course
import redis
#退出页面

class LogoutView(View):
    def get(self,request,*args,**kwargs):
        #logout函数将原本有的用户的信息进行清除
        logout(request)
        return HttpResponseRedirect(reverse("index"))


#登录页面
class LoginView(View):
    #使用的是继承类中的方法
    def get(self,request,*args,**kwargs):
        #动态验证码
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()

        return render(request,'login.html',{
            'login_form':login_form,
            "next":next
        })



    # 使用的是继承类中的方法
    def post(self,request, *args, **kwargs):

        #使用form表单进行登录验证的话，下边的就不需要了
        """
        user_name = request.POST.get("username","") #默认值为空
        password = request.POST.get("password","")
        """

        login_form = LoginForm(request.POST) #获取前端用户输入的内容

        # 用来判断写入的用户名和密码的格式是否正确
        if login_form.is_valid():

            #获取输入的用户名和密码
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]


            #此处我思考了一下，为啥自带的方法知道我肯定有用户名和密码,并且能找到,我想可能是我user
            #模板使用的是继承django本身就有的一个user的模板，所以会相通(个人理解)

            # 用于通过用户密码查询用户是否存在,authenticate是django自带的一个验证方法
            user = authenticate(username=username,password=password)

            if user is not None:
                #自带的方法，查询到用户,根据用户信息，生成sessionid(也就是这个login函数将用户的信息进行存储session)
                login(request,user)
                # reverse,直接使用url中的name，不用再写页面的名字
                next= request.GET.get("next","")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))

            else:
                return render(request,"login.html",{
                    'msg':'用户名或密码错误',
                    'login_form': login_form,

                })

        else:
            return render(request, "login.html", {
                'login_form': login_form,

            })



#手机验证码
class SendSmsView(View):
    #使用的是post请求方式，所以需要下边这个函数模板
    def post(self, request, *args, **kwargs):
        #此处还是使用表单验证的方法
        send_sms_form = DynamicLoginForm(request.POST)
        #判断手机号和动态验证码是否正确
        re_dict = {}  #将信息进行存储
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            #随机生成数字验证码
            code = generate_random(4,0)
            re_json = send_single_sms(yp_apikey,code=code,mobile=mobile)
            #下面当中的变量名称要与前端中的一致
            if re_json['code'] == 0:
                re_dict["status"] = 'success'
                #将数据存入redis中
                r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=0,charset="utf8",decode_responses=True)
                r.set(str(mobile),code)
                r.expire(str(mobile),60*5) #设置验证码五分钟过期

            else:
                re_dict['msg'] = re_json["msg"]
        else:
            #找到表单验证中提示的错误信息（表单验证错误的话会有错误信息）
            for key,value in send_sms_form.errors.items():
                re_dict[key] = value[0]

        return JsonResponse(re_dict) #将得到的信息进行传送，并与前端js进行对比，在页面显示对应的正确或错误信息

#动态登录提交
class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()

        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,

        })
    def post(self, request, *args, **kwargs):

        login_form = DynamicLoginPostForm(request.POST)
        #这个用来判断前端账号登录和手机动态登录的问题
        dynamic_login = True
        if login_form.is_valid():
            #没有注册账号依然可以登录
            mobile = login_form.cleaned_data["mobile"]
            #验证码验证是否正确在forms中写着呢
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]

            else:
                #如果没有，则需要新建一个用户
                user = UserProfile(username=mobile)
                #因为手机验证码登录的用户没有密码，所以需要随机创建一个密码
                password = generate_random(10,2)
                #密码进行加密存储
                user.set_password(password)
                user.mobile=mobile
                user.save()
            # 自带的方法，查询到用户,根据用户信息，生成sessionid(也就是这个login函数将用户的信息进行存储session)
            login(request, user)
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {'login_form': login_form,"dynamic_login":dynamic_login,"d_form":DynamicLoginForm})
#注册页面
class RegisterView(View):
    def get(self,request,*args,**kwargs):
        register_get_form = RegisterGetForm()
        return render(request,'register.html',{"register_get_form":register_get_form})

    def post(self,request,*args,**kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = register_post_form.cleaned_data["mobile"]
            # 验证码验证是否正确在forms中写着呢
            password = register_post_form.cleaned_data["password"]
            #其中判断用户是否存在是在forms中编写
            # 如果没有，则需要新建一个用户
            user = UserProfile(username=mobile)
            # 密码进行加密存储
            user.set_password(password)
            user.mobile = mobile
            user.save()
            # 自带的方法，查询到用户,根据用户信息，生成sessionid(也就是这个login函数将用户的信息进行存储session)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html",
                          {"register_get_form":register_get_form,
                           "register_post_form":register_post_form})


#个人中心
class UserInfoView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        user = request.user
        left_name ='info'
        #修改手机号的随机验证码
        captcha_form = RegisterGetForm()
        return render(request,"usercenter-info.html",{
            "user":user,
            "captcha_form":captcha_form,
            "left_name":left_name
        })
    #用户信息修改
    def post(self, request, *args, **kwargs):
                                                # 如果 instance 有对象则是修改数据 没有就是 新增数据
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(user_info_form.errors)

#个人中心用户修改头像
class UserImageView(LoginRequiredMixin,View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
    #处理用户上传的头像
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse({
                "status":"fail"
            })

#修改密码
class ChangePwdView(View):
    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return JsonResponse({
                    "static":"fail",
                    "msg":"两密码不一致",
                })
            user = request.user
            user.set_password(pwd1)   #set_password自带的保存密码的方法
            user.save()
            #如果不加下边的这个，修改完密码后需要重新登录，加上下边的这个之后，就不用重新登录
            #login(request,user)
            return JsonResponse({
                "status":"success",
            })
        else:
            return JsonResponse(pwd_form.errors)


#修改手机号
class ChangeMobileView(LoginRequiredMixin,View):
    login_url = '/login/'
    def post(self, request, *args, **kwargs):
        update_mobile_form = UpdateMobileForm(request.POST)
        if update_mobile_form.is_valid():
            mobile = update_mobile_form.cleaned_data["mobile"]
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "mobile":"手机号已经存在"
                })
            user = request.user
            user.mobile = mobile
            #登陆的时候使用的用户名是手机号
            user.username = mobile
            user.save()
            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(update_mobile_form.errors)
#我的课程
class MyCourseView(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        my_courses =  UserCourse.objects.filter(user=request.user)
        left_name = 'mycourse'
        return render(request,'usercenter-mycourse.html',{
            "my_courses":my_courses,
            "left_name":left_name
        })


#我的收藏机构
class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)
        left_name = 'myfav'
        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
            "left_name": left_name
        })
#收藏教师
class MyFavTeacherView(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)
        left_name = 'myfav'
        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list":teacher_list,
            "left_name": left_name
        })



    # 收藏教师

class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course = Course.objects.get(id=fav_course.fav_id)
            course_list.append(course)
        left_name = 'myfav'
        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
            "left_name": left_name
        })
#我的消息
class MyMessageView(LoginRequiredMixin,View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        for message in messages:
            message.has_read = True
            message.save()
        # 分页
        try:
            page = request.GET.get('page', 1)  # 这里边的page是前端页面中分页代码中的页面路径中的参数，要与之对应
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, per_page=1, request=request)  # per_page一页显示几个数据
        messages = p.page(page)
        left_name = 'message'
        return render(request,"usercenter-message.html",{
            "messages":messages,
            "left_name":left_name
        })