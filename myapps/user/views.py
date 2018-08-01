import json

from django.shortcuts import render, redirect

# Create your views here.
from user.forms import UserProfileForm
from user.models import UserProfile


def login(request):
    return render(request, 'user/login.html')


def regist(request):
    if request.method == 'GET':
        return render(request, 'user/regist.html')
    else:
        # 读取注册的用户信息
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()  # 验证没有任何问题，则写入数据库
            return redirect('/')  # 重定向到主页
        else:
            errors_json = json.loads(form.errors.as_json())
            return render(request,
                          'user/regist.html',
                          locals())  # locals() 收集当前函数内部的可用对象，生成dict字典