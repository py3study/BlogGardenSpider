#!/usr/bin/env python
# coding: utf-8
import pymysql
import random
import time
import json


class SaveMysql():
    def __init__(self):
		# 这里根据自己后台数据库的字段填写
        self.author = '爬虫自动更新'  # 爬虫自动更新
        self.hits = '0'  # 点击数 默认为0
        self.type_id = '26'   # 类别 即数据库存放的表
        self.keyword = ""   # 关键字为空
        self.create_time = time.strftime("%Y-%m-%d %H:%M:%S")  # 文章更新时间

    def run(self, article_title_summary_content):
        id_number_list = []
        host = 'xxx.xx.xxx.xxx'  # mysql服务器ip地址
        port = 12345  # mysql服务端的端口
        user = 'root'  # mysql服务器用户名
        passwd = 'root'  # mysql服务器密码
        db = 'blog'  # 使用的库名
        conn = pymysql.connect(host=host,
                               user=user,
                               password=passwd,
                               port=port,
                               database=db,
                               charset='utf8',
                               )
        cur = conn.cursor()
        for data in article_title_summary_content:
			# 这里的image_path 是后台的略缩图,没有可以不用加
            self.img_random = random.randint(1, 203)
            self.image_path = "/Public/images/article/thumb/random/{}.jpg".format(self.img_random)  # 略缩图路劲
            self.title = data['title']  # 标题
            self.summary = data['summary']  # 简介
            # 这里json序列化一下，是因为数据库存的是json格式，根据自己后台的需求来改
            self.content = json.dumps(data['content'])  # 文章内容
            # 判断title长度，截取
            if len(self.title) > 20:
                self.title = self.title[0:20]
            # 判断文章简介长度,截取
            if len(self.summary) > 200:
                self.summary = self.summary[0:200]
            # 插入数据
            cur.execute("insert into tbl_article(title, summary, content, author, hits, type_id, image_path,keyword,create_time) \
                  values (%s, %s, %s, %s, %s, %s, %s,%s, %s)", (self.title,self.summary,self.content,self.author,self.hits,self.type_id,self.image_path,self.keyword,self.create_time))
            # 查询插入数据的id
            cur.execute("select id from tbl_article where title='%s' limit 1" % self.title)
            data = cur.fetchone()
            # 获取文章主键id号
            id_number_list.append(data[0])
            conn.commit()
        cur.close()
        conn.close()
        # 返回一个list 里面包含所有文章的id号
        return id_number_list


if __name__ == '__main__':
    pass
