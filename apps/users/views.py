import time

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.urls import reverse
from django.views.generic.base import RedirectView

from users.models import UserProfile


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(RedirectView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html', {'result': ''})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username)
        print(password)
        if all([username, password]):
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
        t = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return render(request, 'login.html', {'result': ('登陆失败' + t)})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username)
        print(password)
        if all([username, password]):
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return render(request, 'index.html')
        t = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return render(request, 'login.html', {'result': ('登陆失败' + t)})

    elif request.method == 'GET':
        return render(request, 'login.html', {'result': ''})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# 3、有时候，某个视图函数是需要经过登录后才能访问的。那么我们可以通过login_required装饰器来实现。
# 在验证失败后，会跳转到/accounts/login/路由。
# (需要修改为自己的登录页面@login_required(login_url='/login/'))
@login_required(login_url='/login/')
def profile(request):
    return HttpResponse("这是个人中心，只有登陆后才能看到！")
