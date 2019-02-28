## 说明
BlogGardenSpider 
博客园文章爬取--更新到自己的博客上(图片下载,url地址替换,css样式替换,自动上传图片,自动插入数据库)

## 如有疑问可加群 198447500

## 项目主要结构
```
./
├── blog_spider.py         # 主程序(文章内容过滤,url地址替换,css样式清洗,图片下载,代理使用)
├── create_dir.py          # 创建层级目录(与线上服务器图片目录对应/年/月/日/)
├── image_processing.py    # 检测图片大小(850,550)--不符合自动修改   
├── mylog.py               # 日志功能,记录爬取过程中的信息
├── resource.py            # 资源文件(包含user-agents，代理ip地址池)
├── ssh_upload.py          # 上传本地地图文件到线上服务器(如目录不存在自动创建,不会覆盖相当于scp -r)
├── update_mysql.py        # 爬取的内容插入到数据库中

```

## 运行环境
| Project | version | Description |
|---------|--------|-------------|
| python  | 3.6.5 | 无 |



## 需要用到的第三方库
selenium   pip3 install selenium   
selenium的使用需要安装谷歌驱动chromedriver.exe，要与本地浏览器的版本一致
下载地址: https://npm.taobao.org/mirrors/chromedriver/
![Image text](https://github.com/py3study/BlogGardenSpider/blob/master/%E5%9B%BE%E7%89%87%E5%8A%A0%E8%BD%BD/222.png)

```
	lxml       pip3 install lxml
	pymysql    pip3 install pymysql
	paramiko   pip3 install paramiko
	PIL        pip3 install pillow
	
```


## 运行截图
![Image text](https://github.com/py3study/BlogGardenSpider/blob/master/%E5%9B%BE%E7%89%87%E5%8A%A0%E8%BD%BD/111.png)


## 动态图
![Image text](https://github.com/py3study/BlogGardenSpider/blob/master/%E5%9B%BE%E7%89%87%E5%8A%A0%E8%BD%BD/blogspider.gif)




## 模块说明
```
	1. 使用ssh_upload时 路径的问题
	   我是win环境上传到linux服务器, 所以需要对"\"路劲做替换，如果是linux对linux传,替换的那一步就不需要了!
	   我这里使用的是id_rsa密钥认证的方式连接的
	   
	
	2. 使用update_mysql时 插入数据的问题
	   我是根据自己mysql表格中的字段,插入数据,这里要结合自己的字段来改!
	   mysql的ip地址,账号,密码,端口 需要改
	
	
	3. 使用resource时，代理ip需要自己写进去
```


## 备注
本项目只是学习爬虫相关的知识，在学习使用中不要太过分(爬全站..)


Copyright (c) 2019-present, Run