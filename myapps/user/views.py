from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'user/login.html')


def regist(request):
    return render(request, 'user/regist.html')