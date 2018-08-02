import json
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.cache import cache_page

from art import tasks
from art.models import Art

# 处理函数中，带有其它参数(artId)
from utils import redis_cache


@cache_page(10)
def show(request, artId):
    # 读取当前用户信息
    login_user = json.loads(request.session.get('login_user'))

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


def advance(request, artId):
    # 抢读
    login_user = request.session.get('login_user')

    if not login_user:
        return JsonResponse({'status': 101,
                             'msg': '亲，请先登录，再抢读,谢谢！'})

    user_id = json.loads(login_user).id
    # 任务延迟执行
    tasks.advanceArt.delay(artId, user_id)
    return JsonResponse({'status': 201,
                         'msg': '正在抢读...'})


def queryAdvance(request, artId):
    # 查询抢读是否成功
    login_user = request.session.get('login_user')

    if not login_user:
        return JsonResponse({'status': 101,
                             'msg': '亲，请先登录，再查看抢读,谢谢！'})
    user_id = json.loads(login_user).id

    artId = redis_cache.hget('AdvanceArt', user_id)
    if artId:
        art = Art.objects.get(id=artId.decode())
        return JsonResponse({'status': 200,
                             'msg': '恭喜您，抢读％s 成功' %art.title})
    else:
        if redis_cache.hlen('AdvanceArt')< 5:
            return JsonResponse({'status': 202,
                                 'msg': '正在抢读...'})
        else:
            return JsonResponse({'status': 203,
                                 'msg': '抢读失败， 请下次碰碰运气！'})