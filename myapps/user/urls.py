from django.conf.urls import url

from user import views

app_name = 'user'

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^regist/', views.regist),
    url(r'^upload/', views.upload),

]
