import os
from time import sleep
command='apt -y install python3-pip'
os.system(command)
sleep(1)
command='pip3 install paramiko'
os.system(command)
sleep(1)
import paramiko
command='apt -y install wget'
os.system(command)
sleep(1)
command='wget https://raw.githubusercontent.com/0honus0/test/main/bendi.py'
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
chan.send('screen -S bendi\n')
sleep(2)
chan.send('cd /root\n')
sleep(1)
chan.send('python3 bendi.py\n')
sleep(1)
print('OK')
