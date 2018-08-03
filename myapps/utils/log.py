import logging

# 配置root 日志记录器

logging.getLogger().setLevel(logging.INFO)

# 日志格式化
formatter = '[%(asctime)s->%(module)s->%(funcName)s at %(lineno)d]%(message)s'

# 设置root的基本格式
logging.basicConfig(format=formatter,
                    datefmt='%Y-%m-%d %H:%M:%S')
