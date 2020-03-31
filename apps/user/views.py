from django.shortcuts import render,redirect
import re
from django.core.urlresolvers import reverse
from apps.user.models import User
# Create your views here

#/user/register
def register(request):
    '''显示注册页面'''
    return render(request,'register.html')

def register_handle(request):
    '''注册处理'''
    #接受数据
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')

    #数据校验
    if not all([username,password,email]):
        return render(request,'register.html',{'errmsg':'数据不完整'})

    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request, 'register.html', {'errmsg': '邮箱不对'})

    if allow is not 'on':
        return render(request,'register.html',{'errmsg':'请同意协议'})

    #进行业务处理：注册
    # User.user()
    # user.username = username
    # user.password = password
    # ...
    # user.save()

    #django内置认证系统
    user = User.objects.create_user(username,email,password)

    #返回应答  跳转首页

    return redirect(reverse('goods:index'))


