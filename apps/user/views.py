from django.shortcuts import render,redirect
import re
from django.urls import reverse
from apps.user.models import User
from django.views.generic import View
from django.conf import  settings
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.http import HttpResponse
# from django.core.mail import send_mail
from apps import goods
from django.contrib.auth import authenticate,login
from celery_tasks.tasks import send_register_active_email
# Create your views here

#/user/register
def register(request):
    '''显示注册页面'''
    if request.method == 'GET':

        return render(request,'register.html')
    else:
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据校验
        if allow != 'on':
            return  render(request, 'register.html',{'errmsg':'未同意用户协议'})


        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})


        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return render(request, 'register.html', {'errmsg': '邮箱不对'})

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            User.username = None

        if User.username is not None:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理：注册

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 返回应答  跳转首页
        return redirect(reverse('goods:index'))

class RegisterView(View):
    '''注册'''
    def get(self,request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self,request):
        '''进行注册处理'''
        # 接受数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 数据校验
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '未同意用户协议'})

        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱不对'})

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            User.username = None

        if User.username is not None:
            return render(request, 'register.html', {'errmsg': '用户名已存在'})

        # 进行业务处理：注册

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        #发送激活邮件，包含激活连接： http://127.0.0.1:8000/user/active/1    加密  username
        #激活连接需要包含用户的身份信息  且身份信息加密

        # 加密用户身份信息 ，生成激活token
        serializer = Serializer(settings.SECRET_KEY,600)
        info = {'confirm':user.id}
        token = serializer.dumps(info).decode('utf8')

        #发邮件
        subject = '天天生鲜欢迎信息'
        message = '<h1></h1>'
        sender = settings.EMAIL_FROM
        receiver = [email]

        send_register_active_email.delay(email,username,token)


        # 返回应答  跳转首页
        return redirect(reverse('goods:index'))

class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行用户激活'''
        #进行解密，获取激活信息
        serializer = Serializer(settings.SECRET_KEY, 600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))

        except SignatureExpired as e :
            #激活连接过期
            return HttpResponse('激活链接已过期')


class LoginView(View):
    '''登陆'''
    def get(self,request):
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request):
        '''登录校验'''

        #接受数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        #校验数据
        if not all([username,password]):
            return render(request, 'login.html',{'errmsg':'数据不完整'})


        user = authenticate(username=username,password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户激活
                # 记录用户的登录状态
                login(request,user)
                response = redirect(reverse('goods:index'))
                remember = request.POST.get('remember')

                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')

                return response

            else:
                # 用户未激活
                return render(request,'login.html',{'errmsg':'账户未激活'})
        else:
            #用户名或密码错误
            return render(request,'login.html',{'errmsg':'用户名或者密码错误'})

# user
class UserInfoView(View):
    '''用户中心-信息页'''
    def get(self,requset):
        '''显示'''
        return render(requset,'user_center_info.html',{'page':'user'})

# user/order
class UserOrderView(View):
    '''用户中心-订单页'''
    def get(self,requset):
        '''显示'''
        return render(requset,'user_center_order.html',{'page':'order'})

# user/address
class AddressView(View):
    '''用户中心-地址页'''
    def get(self,requset):
        '''显示'''
        return render(requset,'user_center_site.html',{'page':'address'})






