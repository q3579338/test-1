'''
Author: your name
Date: 2021-01-08 16:42:16
LastEditTime: 2021-01-08 20:40:10
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \python\project\new\begin.py
'''
import os
from time import sleep
import paramiko

command='apt -y install wget'
os.system(command)
sleep(1)
command='wget https://raw.githubusercontent.com/0honus0/test/main/tmp.py'
os.system(command)
sleep(1)
try:
    username='root'
    port= 22
    ip='127.0.0.1'
    password=''
    client=paramiko.SSHClient()
    key=paramiko.AutoAddPolicy()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, password=password,timeout=30)
except:
    print('Failed')
chan = client.invoke_shell()
chan.send('screen -S ip\n')
sleep(2)
chan.send('cd /root\n')
sleep(1)
chan.send('python3 tmp.py\n')
sleep(1)
print('OK')