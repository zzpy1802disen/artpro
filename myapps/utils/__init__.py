# '''
# 多模块之间的工具包
# '''
import logging
import os

from MArtPro import settings


def mvImage(filePath, dstDir):
    logging.info(filePath)
    logging.info(dstDir)
    '''
    将filePath位置的文件，移动到dstDir目录下
    :param filePath:
    :param dstDir:
    :return:
    '''
    # 读取到文件名
    tmpDir, fileName = os.path.split(filePath)

    with open(filePath, 'rb') as rf:
        with open(os.path.join(dstDir, fileName), 'wb') as wf:
            wf.write(rf.read())

    # 清空临时目录
    for tmpFilePath in os.listdir(tmpDir):
        os.remove(os.path.join(tmpDir, tmpFilePath))

    return fileName


def mvImageFromTmp(filePath):
    dstDir = os.path.join(settings.BASE_DIR, 'static/users')
    srcPath = os.path.join(settings.BASE_DIR, filePath[1:])

    return os.path.join('/static/users', mvImage(srcPath, dstDir))