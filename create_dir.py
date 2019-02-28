#!/usr/bin/env python3
# coding: utf-8
import time
import os


class Create(object):
    def __init__(self):
        # 获取项目根目录
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def folder(self):
        """
        创建年/月/日 文件夹
        :return: bool
        """
        # 系统当前时间年份
        year = time.strftime('%Y', time.localtime(time.time()))
        # 月份
        month = time.strftime('%m', time.localtime(time.time()))
        # 日期
        day = time.strftime('%d', time.localtime(time.time()))

        root_path = os.path.join(self.BASE_DIR, 'picture')  # 根目录
        # print(root_path)
        if not os.path.exists(root_path):  # 判断跟目录是否存在
            os.makedirs(root_path)

        fileYear = os.path.join(self.BASE_DIR, 'picture', year)
        fileMonth = os.path.join(fileYear, month)
        fileDay = os.path.join(fileMonth, day)

        # 判断目录是否存在，否则创建
        try:
            if not os.path.exists(fileYear):
                os.mkdir(fileYear)
                os.mkdir(fileMonth)
                os.mkdir(fileDay)
            else:
                if not os.path.exists(fileMonth):
                    os.mkdir(fileMonth)
                    os.mkdir(fileDay)
                else:
                    if not os.path.exists(fileDay):
                        os.mkdir(fileDay)

            # 年月日路径的绝对路径
            path = os.path.join(self.BASE_DIR, 'picture', year, month, day)
            isExists = os.path.exists(path)  # 判断路径是否存在

            # 判断结果
            if not isExists:
                # 如果不存在则创建目录
                os.makedirs(path)

            return path  # 返回创建的年月日绝对路径
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    res = Create().folder()
    print(res)
