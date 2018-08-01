from django.db import models

# Create your models here.
class UserProfile(models.Model):
    username = models.CharField(max_length=20,
                                verbose_name='用户名')
    password = models.CharField(max_length=50,
                                verbose_name='口令')
    email = models.CharField(max_length=50,
                             verbose_name='邮箱')

    phone = models.CharField(max_length=12,
                             verbose_name='手机号')

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name