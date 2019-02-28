#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from lxml import etree  # 解析html模块(数据清洗,数据整合)
import time
import urllib.request  # 获取html内容
import os
import string
import re
import copy
import random  # 随机取浏览器头和代理ip
import resource  # 代理模块包含(浏览器头列表池,代理ip地址池)
from update_mysql import SaveMysql  # 保存到mysql
from create_dir import Create  # 创建层级目录,存放图片  return绝对路径
from ssh_upload import upload  # 上传文件到远程服务器
from image_processing import ImageProcessing  # 检查图片尺寸大小是否符合规定，不符合修改尺寸大小
from mylog import MyLog as mylog  # 日志模块,记录爬取的日志信息


class GetCnblogs:
    def __init__(self, url):
        self.log = mylog()  # 实例化mylog类,用于记录日志
        self.save_mysql = SaveMysql()  # 实例化SaveMysql类，数据存储
        self.create_dir = Create()
        self.url = url

        # 设置浏览器打开目标网站 self.browser = browser
        self.browser = self.setup_browser(self.url)

        # 返回包含title,article_info,url的字典
        self.title_url_dict = self.simulated_click(self.browser)

        # 返回一个list[{},{},{}]
        self.html = self.get_html_content(self.title_url_dict)

        # 返回一个list[{},{},{}],利用lxml-xpath对每篇文章过滤，只保留内容部分
        self.clean_content = self.data_location(self.html)

        # 返回一个list[{},{},{}] 数据清洗(包括图片下载,图片地址替换)
        self.replace_url_content = self.data_clean_and_data_integration(self.clean_content)

        # 返回一个list[{},{},{}] 数据清洗(替换css样式)
        self.content = self.replace_css(self.replace_url_content)

        # 保存到数据库
        for i in self.content:
            self.log.info("爬取博客园文章:{}\n往数据库中插入标题为:{}\n博客简介为:{}\n博客内容为:{}\n文章作者:{}".format(i['title'],
                                                                                          i['title'],
                                                                                          i['summary'],
                                                                                          '内容太多忽略.....', '爬虫自动更新'))
        #  得到mysql查询主键id值
        # 返回一个list[id,id,id]
        self.id_number_list = self.save_mysql.run(self.content)
        for i in self.id_number_list:
            self.log.info("文章已插入成功\n可以访问查看:http://www.py3study.com/Article/details/id/{}.html".format(i))
        self.log.info("数据插入结束")

    def setup_browser(self, url):
        """
        打开目标网站 https://www.cnblogs.com/
        :return: browser
        """
        try:
            # 创建chrome参数对象
            options = webdriver.ChromeOptions()
            # 设置为无头模式
            options.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=options)
            # 利用selenium打开网站
            browser.get(url)
            # 等待网站js代码加载完毕
            browser.implicitly_wait(20)
        except Exception as e:
            # 记录错误日志
            self.log.error('打开目标网站失败:{},错误代码:{}'.format(url, e))
        else:
            # 记录成功日志
            self.log.info('打开目标网站成功:{}'.format(url))
            # 返回实例化selenium对象
            return browser

    def simulated_click(self, browser):
        """
        获取编程语言--python 技术文章
        :param browser:
        :return: title_url_dict  包含title,url的字典
        """
        # 获取文章title, 文章简介, url地址,
        title_list = []
        url_list = []
        article_info_list = []
        title_article_url_dict = {}
        # 获取标题
        for i in browser.find_elements_by_xpath("//div[@class='post_item']/div[@class='post_item_body']/h3/a"):
            title_list.append(i.text)
        # 获取文章简介
        for i in browser.find_elements_by_xpath("//div[@class='post_item']/div[@class='post_item_body']/p"):
            article_info_list.append(i.text)
        # 获取文章url地址
        for i in browser.find_elements_by_xpath("//div[@class='post_item']/div[@class='post_item_body']/h3/a"):
            url_list.append(i.get_attribute('href'))
        # 数据合并: title_list标题列表, article_info_list文章详情列表, url_list网站地址列表
        # 构建字典
        # title_article_url_dict = {
        # 1:{'title':'xxx', 'article_info':'xxxx', 'url':'xxx'},
        # 2: {'title':'xxx', 'article_info':'xxxx', 'url':'xxx'},
        # 3: {'title':'xxx', 'article_info':'xxxx', 'url':'xxx'},
        # }
        i = 1
        for x in title_list:
            title_article_url_dict.setdefault(i)
            title_article_url_dict[i] = {'title': x, 'article_info': None, 'url': None}
            i += 1
        n = 1
        for z in article_info_list:
            title_article_url_dict[n]['article_info'] = z
            n += 1
        s = 1
        for y in url_list:
            title_article_url_dict[s]['url'] = y
            s += 1
        time.sleep(1)
        browser.quit()
        return title_article_url_dict

    def get_html_content(self, title_article_url_dict):
        """
        获取每篇python文章的html_content
        :param title_article_url_dict:
        :return: html
        """
        # 创建一个包含{'title':None, 'summary':None, 'content':None}
        # [{'title':None, 'summary':None, 'content':None},{'title':None, 'summary':None, 'content':None}]
        article_title_summary_content_list = []
        article_title_summary_content = {}

        for i in title_article_url_dict:
            """从页面返回数据"""
            fakeHeaders = {"User-Agent": self.getRandomHeaders()}
            request = urllib.request.Request(title_article_url_dict[i]['url'], headers=fakeHeaders)
            proxy = urllib.request.ProxyHandler({'http': 'http://' + self.getRandomProxy()})
            opener = urllib.request.build_opener(proxy)
            urllib.request.install_opener(opener)
            try:
                response = urllib.request.urlopen(request)
                html = response.read()
                time.sleep(1)
            except Exception as e:
                self.log.error('获取标题:{}的html数据失败,{}'.format(title_article_url_dict[i]['title'], e))
            else:
                self.log.info('获取标题:{}的html数据成功'.format(title_article_url_dict[i]['title']))
                article_title_summary_content['title'] = title_article_url_dict[i]['title']
                article_title_summary_content['summary'] = title_article_url_dict[i]['article_info']
                article_title_summary_content['content'] = html
                # 这里踩了坑,用了深copy来确保article_title_summary_content的内存地址不一样
                article_title_summary_content_list.append(copy.deepcopy(article_title_summary_content))
        return article_title_summary_content_list

    def getRandomProxy(self):
        # 随机获取Proxy代理ip
        return random.choice(resource.PROXIES)

    def getRandomHeaders(self):
        # 随机获取UserAgent头
        return random.choice(resource.UserAgents)

    def data_location(self, article_title_summary_content_list):
        """
        利用etree-xpath 做数据定位
        :param article_title_summary_content:
        :return: 只保留文章内容部分(过滤掉没有的)
        """
        for i in article_title_summary_content_list:
            # article_title_summary_content['content'].decode('utf-8').encode('utf-8')
            html_xpath = etree.HTML(i['content'])
            html_content = html_xpath.xpath("//div[@id='cnblogs_post_body']")  # xpath返回一个列表
            filter_content = etree.tostring(html_content[0], encoding="utf-8", pretty_print=True, method="html")
            i['content'] = filter_content.decode('utf-8')
        return article_title_summary_content_list

    def data_clean_and_data_integration(self, article_title_summary_content):
        """
        数据清洗
        找到所有文章的图片下载地址,下载图片并按照数据库文章图片路径存储
        构建图片地址替换字典
        把html_content里面的图片地址替换成线上服务器的图片路径地址
        :param article_title_summary_content:
        :return: article_title_summary_content
        """
        try:
            number = 0
            for data in article_title_summary_content:
                img_url_dict_old = {}
                img_url_dict_new = {}
                html_content = etree.HTML(data['content'])
                # 图片地址列表
                image_list = html_content.xpath("//div[@id='cnblogs_post_body']//img/@src")
                if image_list:
                    # 创建目录名,按day来创建
                    year = time.strftime('%Y', time.localtime(time.time()))  # 年
                    month = time.strftime('%m', time.localtime(time.time()))  # 月
                    dirname_day = time.strftime('%d', time.localtime(time.time()))  # 日
                    dir_path = self.create_dir.folder()  # 创建存储图片目录
                    os.chdir(dir_path)
                    n = 1
                    for i in image_list:
                        suffix_name = os.path.splitext(i)[1]  # 获取img后缀名
                        # 随机生成一个32位字符串与后缀名拼接,作为img的完整名
                        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
                        img_name = ran_str + suffix_name  # 完整img名字
                        # 线上服务器图片地址
                        server_img_url = '/Public/images/article/picture/{}/{}/{}/{}'.format(year, month, dirname_day,
                                                                                             img_name)
                        # 下载图片:  需要两个参数(图片下载路径,图片名)
                        try:
                            urllib.request.urlretrieve(i, img_name)
                        except Exception as e:
                            self.log.info("下载异常:{}".format(e))

                        # 判断图片大小是否符合规定，需要传两个参数(图片绝对路径,图片名)
                        ImageProcessing(dir_path, img_name)
                        time.sleep(3)
                        # 构建图片地址替换字典
                        # 博客园 old = {1:'url',2:'url'}
                        # 线上服务器 new = {1: 'server_img_url', 2:'server_img_url'}
                        img_url_dict_old[n] = i
                        img_url_dict_new[n] = server_img_url
                        n += 1
					# 替换url地址
                    for x in img_url_dict_old:
                        for y in img_url_dict_new:
                            if x == y:
                                article_title_summary_content[number]['content'] = \
                                article_title_summary_content[number]['content'].replace(img_url_dict_old[x],
                                                                                         img_url_dict_new[y])
                else:
                    self.log.info("{}文章没有图片".format(data['title']))
                number += 1
            self.log.info("所有图片下载到本地完毕")
            # 切回根目录
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            # 上传文件到远程服务器,并递归删除本地创建目录
            res = upload()
            if res:
                self.log.info("上传图片到服务器成功")
            else:
                self.log.info("上传图片到服务器失败")
            self.log.info("替换文章图片url地址,清洗url数据完毕")
            return article_title_summary_content

        except Exception as e:
            self.log.info(e)
            return article_title_summary_content

    def replace_css(self, article_title_summary_content):
        try:
            number = 0
            for data in article_title_summary_content:
                # 构建博客园css样式替换字典{'1':'span style="color: #008080;"', '2':'span style="color: #457554;"',...}
                boke_css_dict = {}
                html_content = etree.HTML(data['content'])
                # 找到所pce标签下面的span标签
                css_list = html_content.xpath("//pre")
                n = 1
                if css_list:
                    for i in css_list:
                        pre_label = etree.tostring(i, encoding="utf-8", pretty_print=True, method="html")
                        pre_label = pre_label.decode('utf-8')
                        # pre_label 博客园pre css样式
                        res_list = re.findall(r'span\s+style="([^"]+?)"', pre_label)
                        # 服务器上的 pre css样式  'span class="hljs-keyword"'
                        if res_list:
                            for x in res_list:
                                boke_css_dict[str(n)] = x
                                for y in boke_css_dict:
                                    article_title_summary_content[number]['content'] = \
                                    article_title_summary_content[number]['content'].replace(
                                        boke_css_dict[y], 'span class="hljs-keyword"')
                        else:
                            self.log.info('标题为{}的第{}pre标签,不需要替换css样式'.format(article_title_summary_content[number]['title'], n))
                        n += 1
                else:
                    self.log.info("{}文章没有pre标签,不需要替换css样式".format(article_title_summary_content[number]['title']))
                number += 1
            self.log.info("清洗css数据完毕")
            return article_title_summary_content
        except Exception as e:
            self.log.info(e)
            return article_title_summary_content


if __name__ == '__main__':
    # 后面的5 表示第5页
    url = 'https://www.cnblogs.com/cate/python/5'
    st = GetCnblogs(url)

    # 如果需要爬取多页 则可以写成下面这样
    # 博客园最多200页
    # for i in range(1, 200):
    #     url = 'https://www.cnblogs.com/cate/python/' + str(i)
    #     st = GetCnblogs(url)
