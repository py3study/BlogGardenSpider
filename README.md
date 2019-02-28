## 说明
BlogGardenSpider 
博客园文章爬取--更新到自己的博客上(图片下载,url地址替换,css样式替换,自动上传图片,自动插入数据库)

## 项目主要结构
```
./
├── blog_spider.py         # 主程序(文章内容过滤,url地址替换,css样式清洗,图片下载,代理使用)
├── create_dir.py          # 创建层级目录(与线上服务器图片目录对应/年/月/日/)
├── image_processing.py    # 检测图片大小(850,550)--不符合自动修改   
├── mylog.py               # 日志功能,记录爬取过程中的信息
├── resource.py            # 资源文件(包含user-agents，代理ip地址池)
├── ssh_upload.py          # 上传本地地图文件到线上服务器(mkdir -p)
├── update_mysql.py        # 爬取的内容插入到数据库中

```

## 运行环境
| Project | version | Description |
|---------|--------|-------------|
| python  | 3.6.5 | 无 |



## 需要用到的第三方库
```
	selenium   pip3 install selenium   
	           selenium的使用需要安装谷歌驱动chromedriver.exe，要与本地浏览器的版本一直
		       下载地址: https://npm.taobao.org/mirrors/chromedriver/
			   
		
	lxml       pip3 install lxml
	pymysql    pip3 install pymysql
	paramiko   pip3 install paramiko
	PIL        pip3 install pillow
	
```


## 效果
首页：

![Image text](https://github.com/py3study/AutoCmdb/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/%E9%A6%96%E9%A1%B5.png)

ansible管理：

![Image text](https://github.com/py3study/AutoCmdb/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/ansible%E7%AE%A1%E7%90%86.png)

ansible主机：

![Image text](https://github.com/py3study/AutoCmdb/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/ansible%E4%B8%BB%E6%9C%BA.png)

主机详情：

![Image text](https://github.com/py3study/AutoCmdb/blob/master/%E6%95%88%E6%9E%9C%E5%9B%BE/%E4%B8%BB%E6%9C%BA%E8%AF%A6%E6%83%85.png)


## 运行方式
### ansible主控端
```
首先需要编译安装python3,请参考链接:
http://www.py3study.com/Article/details/id/320.html
做到添加豆瓣源为止,请务必按照本教程操作,否则会出现没有pip3的问题!!!

安装2个系统软件
yum install -y ansible expect


安装python相关模块
pip3 install django==1.11.15
pip3 install djangorestframework
pip3 install ansible
或者使用requirements.txt文件安装相关模块
pip3 install -r requirements.txt

最后切换到项目目录,使用以下命令运行
python3 manage.py runserver 0.0.0.0:8000
```
### ansible被控端
```
编译安装python3,参考上面的操作!
注意：被控端不需要安装ansible!!!

安装python相关模块
pip3 install requests psutil

将项目中的ansible_client拷贝到opt目录中
注意：务必修改cpu.py和memory.py中的ip地址

设置linux任务计划:

# 监控cpu和内存
* * * * * python3 /opt/ansible_client/monitor/cpu.py
* * * * * python3 /opt/ansible_client/monitor/memory.py
```

## 网页操作
```
请务必安装以下操作进行：
访问页面： http://ip地址/web/  
注意：必须使用谷歌浏览器访问,360浏览器可能某些数据无法加载！

1. 进入首页,点击左侧ansible管理。必须先添加组
2. 添加组之后,再点击添加主机
3. 最后点击左侧ansible主机,就可以查看主机详情和监控图表了
```


## 备注
本项目只是一个demo,请勿直接用于生产环境!


Copyright (c) 2018-present, xiao You