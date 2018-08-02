# 声明 Celery应用对象
from __future__ import absolute_import
import os

from celery import Celery


from MArtPro import settings

# 设置环境变量 DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MArtPro.settings')

app = Celery('ArtCelery')  # 创建Celery应用

# 配置Celery应用对象
app.config_from_object('django.conf:settings')

# 自动查找当前项目中的Celery的Task（异步函数）
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
