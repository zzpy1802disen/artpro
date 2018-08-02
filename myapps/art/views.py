import time
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from art.models import Art

# 处理函数中，带有其它参数(artId)
from utils import redis_cache


@cache_page(10)
def show(request, artId):
    # 查看指定的文章
    art = Art.objects.get(id=artId)

    # 收集文章阅读情况
    redis_cache.zincrby('rankTop5', artId)

    # 获取阅读量排名前5的文章
    rankArtTop = listRankTop(5)

    return render(request, 'art/show.html', locals())


# 返回 [(<Art>, 4), (<Art>, 3),...]

def listRankTop(top):
    # 读取文章排行(id , score)
    rank_ids = redis_cache.zrevrange('rankTop5', 0, top-1, withscores=True)
    ids = [int(id.decode()) for id, score in rank_ids]

    # 根据ids 查找所有文章
    rank_arts = Art.objects.in_bulk(ids)  # 返回 {id: Art}

    # 根据rank_ids和rank_arts 生成 返回结果
    return [(rank_arts.get(int(id.decode())), int(score)) for id, score in rank_ids]
