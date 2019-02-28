#!/usr/bin/env python
# coding: utf-8

from PIL import Image
import os


class ImageProcessing:
    def __init__(self, img_path, img_name):
        self.img_path = img_path
        self.img_name = img_name
        self.img_method()

    def img_method(self):
        # 拼接图片绝对路径
        img_abs_path = os.path.join(self.img_path, self.img_name)
        im = Image.open(img_abs_path)
        length, width = im.size
		# 设定图片长<850,宽<550
        if length < 850 and width < 550:
            im.close()
        if length > 850 and width < 550:
            im.thumbnail((850-1, width))
            os.remove(img_abs_path)
            im.save(self.img_name)
            im.close()
        if length < 850 and width > 550:
            im.thumbnail((length, 550-1))
            os.remove(img_abs_path)
            im.save(self.img_name)
            im.close()
        if length > 850 and width > 550:
            im.thumbnail((850-1, 550-1))
            os.remove(img_abs_path)
            im.save(self.img_name)
            im.close()


if __name__ == '__main__':
    ImageProcessing(r'D:\text', '1.png')



