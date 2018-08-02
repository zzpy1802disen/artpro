"""MArtPro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
import json

from django.shortcuts import render

import xadmin as admin
from django.conf.urls import url, include

# 主页请求处理的view函数
from art.models import Art


def toIndex(request):
    lu = request.session.get('login_user')
    if lu:
        login_user = json.loads(lu)

    # 加载所有文章
    arts = Art.objects.all()

    return render(request, 'index.html', locals())


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^user/', include('user.urls')),  # 引入user模块的urls.py
    url(r'^', toIndex),  # 引入user模块的urls.py

]
