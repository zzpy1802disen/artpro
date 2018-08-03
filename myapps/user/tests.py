from django.test import TestCase

# Create your tests here.
from utils import log
import logging


class TestLog(TestCase):
    def testLog(self):
        self.assertEquals(1, 1)
        logging.warning('1=1是ok')

    def testUser(self):
        self.assertEquals('disen', 'disen')

        # 获取info的日志记录器
        logging.getLogger('info').warning('haha')
