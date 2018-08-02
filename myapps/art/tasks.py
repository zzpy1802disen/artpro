from MArtPro.celery import app
from utils import redis_cache


@app.task
def advanceArt(artId, userId):
    # 抢读文章(artId 文章id, userId 当前用户登录的Id)
    print('用户', userId, '正在抢读', artId)

    # 判断当前抢读的hash对象AdvanceArt长度是否达到5个
    if redis_cache.hlen('AdvanceArt') >= 5:
        return artId + '抢读失败'

    redis_cache.hset('AdvanceArt', userId, artId)

    return artId + '抢读成功!'


@app.task
def sendEmailLog():
    # 读取指定日志文件的内容，并发送给管理员
    print('已发送邮箱')
    return '日志邮箱已发送'