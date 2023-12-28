# 开发者：Annona
# 开发时间：2023/6/6 14:40

# import paramiko
#
# # 创建SSH客户端
# client = paramiko.SSHClient()
# # 自动添加远程服务器的主机密钥
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接远程服务器
# client.connect('191.168.0.213', username='Administrator', password='5*dr2bTG#B')
#
# # 打开远程文件
# remote_file = client.open('')
# # 读取文件内容
# content = remote_file.read()
# # 输出文件内容
# print(content)
# # 关闭远程文件
# remote_file.close()
# # 关闭SSH连接
# client.close()
import datetime
import os

