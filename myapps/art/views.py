from django.shortcuts import render

# Create your views here.
from art.models import Art

def show(request, artId):
    # 查看指定的文章
    art = Art.objects.get(id=artId)
    return render(request, 'art/show.html', locals())