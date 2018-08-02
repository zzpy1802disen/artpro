import json
import uuid

import os

from django.contrib.auth.hashers import make_password, check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from MArtPro import settings
from user.forms import UserProfileForm
from user.models import UserProfile

from utils import mvImageFromTmp


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 查询此用户是否存在
        queryset = UserProfile.objects.filter(username=username)
        if queryset.exists():
            user = queryset.first()

            # 验证口令是否正确
            if check_password(password, user.password):
                login_user = json.dumps({'id': user.id,
                                         'name': user.username,
                                         'photo': user.photo})

                request.session['login_user'] = login_user
                return redirect('/')
            else:
                error_msg = '用户名或口令不正确'
        else:
            error_msg = '用户 %s 不存在' % username

    return render(request, 'user/login.html', locals())


def regist(request):
    if request.method == 'GET':
        return render(request, 'user/regist.html')
    else:
        # 读取注册的用户信息
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save()  # 验证没有任何问题，则写入数据库

            # 清除上传图片的临时目录
            photo = request.POST.get('photo')
            if photo:
                mvFilePath = mvImageFromTmp(photo)
                user.photo = mvFilePath
                user.save()  # 更新目录

            # 将当前注册成功的用户名和id写入到session中
            request.session['login_user'] = json.dumps({'id': user.id,
                                                        'name': user.username,
                                                        'photo': user.photo})

            return redirect('/')  # 重定向到主页
        else:
            errors_json = json.loads(form.errors.as_json())
            return render(request,
                          'user/regist.html',
                          locals())  # locals() 收集当前函数内部的可用对象，生成dict字典


# 实现文件上传的前端ajax接口
# @csrf_exempt 不验证csrf 跨域问题
@csrf_exempt
def upload(request):
    print(request.method, request.POST)
    print(request.FILES)

    # 获取上传的图片
    uImage: InMemoryUploadedFile = request.FILES.get('u_img')

    # 生成新的文件名
    imgFileName = str(uuid.uuid4()).replace('-', '') + os.path.splitext(uImage.name)[-1]

    # 指定新的文件保存的位置
    imgFilePath = os.path.join(settings.MEDIA_ROOT, 'user/' + imgFileName)

    with open(imgFilePath, 'wb') as f:
        # 按上传文件的段，写入到新的文件中
        for chunk in uImage.chunks():
            f.write(chunk)

    return JsonResponse({'path': '/static/uploads/user/' + imgFileName,
                         'status': 'ok'})


def logout(request):
    # 删除session（字典）中的login_user
    # del request.session['login_user']
    request.session.flush()
    return redirect('/')
