#!/usr/bin/env python
# coding: utf-8
import logging
import getpass
import sys


# 定义MyLog类
class MyLog(object):
    def __init__(self):
        self.user = getpass.getuser()  # 获取用户
        self.logger = logging.getLogger(self.user)
        self.logger.setLevel(logging.DEBUG)

        # 日志文件名
        self.logfile = sys.argv[0][0:-3] + '.log'  # 动态获取调用文件的名字
        self.formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(message)-12s\r\n')

        # 日志显示到屏幕上并输出到日志文件内
        self.logHand = logging.FileHandler(self.logfile, encoding='utf-8')
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.DEBUG)

        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.DEBUG)

        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)

    # 日志的5个级别对应以下的5个函数
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


if __name__ == '__main__':
    mylog = MyLog()
    mylog.debug(u"I'm debug 中文测试")
    mylog.info(u"I'm info 中文测试")
    mylog.warn(u"I'm warn 中文测试")
    mylog.error(u"I'm error 中文测试")
    mylog.critical(u"I'm critical 中文测试")
