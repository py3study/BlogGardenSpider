#!/usr/bin/env python3
# coding: utf-8
import paramiko
import os
import shutil

# 连接远程服务器
def upload():
    ip = "xxx.xxx.xxx.xxx"
    port = 1234
    user = "root"
    # 本地创建的图片存放路径,这里我是win环境
    local_dir = r"D:\picture"
    # 线上服务器的图片存放路径
    remote_dir = "/tmp/picture"
   
    try:
        # 本地密钥文件路径[此文件服务器上~/.ssh/id_rsa可下载到本地]
        pkey = r'D:\id_rsa_py3.py3'
        key = paramiko.RSAKey.from_private_key_file(pkey, password='root')  # 有解密密码时
        ssh = paramiko.SSHClient()
        # 通过公共方式进行认证 (不需要在known_hosts 文件中存在)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 这里要 pkey passwordkey 密钥文件 注意password参数必带,内容可以为空
        # timeout 指定超时时间，如果网络不好，务必指定超时时间
        ssh.connect(ip, port, user, password='******', timeout=10, pkey=key)
        sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
        # os.walk返回生成器，遍历本地目录下的所有文件
        for root, dirs, files in os.walk(local_dir):
            for filespath in files:  # 判断是文件时
                local_file = os.path.join(root, filespath)  # 拼接本地文件绝对路径
                a = local_file.replace(local_dir, '')  # 替换上级目录
                a = a.replace('\\', '/')  # windows路径的\ 替换为linux的 /
                remote_file = remote_dir + a  # 拼接linux路径
                try:
                    sftp.put(local_file, remote_file)  # 正常 put上传文件
                except Exception as e:  # 遇到异常情况下，也就是远程目录不存在时
                    catalog = os.path.split(remote_file)[0]  # 远程目录
                    # 使用mkdir -p 创建远程目录，get_pty表示提升权限
                    ssh.exec_command("mkdir -p %s" % catalog, get_pty=True)
                    sftp.put(local_file, remote_file)
            for name in dirs:  # 判断是目录时
                local_path = os.path.join(root, name)
                a = local_path.replace(local_dir, '')
                remote_path = os.path.join(remote_dir, a)
                try:
                    sftp.mkdir(remote_path)
                except Exception as e:  # 出现Failure时
                    pass  # 不要输出Failure
        # 递归删除目录以及文件
        shutil.rmtree(local_dir)
        return True
    except Exception as e:
        print(e)
        # 递归删除目录以及文件
        shutil.rmtree(local_dir)
        return False


if __name__ == '__main__':
    res = upload()
    if res:
        print("上传图片到服务器成功")
    else:
        print("上传图片到服务器失败")
