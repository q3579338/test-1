'''
Author: honus
Date: 2021-10-11 19:26:54
LastEditTime: 2021-10-12 12:58:08
LastEditors: honus
Description: 还原ip port设置 从btfs2开始到btfs5
FilePath: /test/restore_ip.py
'''
import os
import paramiko
from time import sleep

command='curl ifconfig.me'
res=os.popen(command).readlines()
ip=res[0]
print(ip)

def GetPort(count):
    return 4000+count

suc=False
try:
    username='root'
    port= 22
    password=''
    client=paramiko.SSHClient()
    key=paramiko.AutoAddPolicy()
    client.set_missing_host_key_policy(key)
    client.connect(ip, port, username=username, password=password,timeout=30)
    suc=True
except:
    print('con fail')

if not suc:
    os._exit(0)

count=2
while count<=5:
    chan = client.invoke_shell()
    chan.send('cd /root\n')
    sleep(1)
    command='export BTFS_PATH=/root/.btfs'+str(count)+'\n'
    print(command)
    chan.send(command)
    sleep(2)
    command='export PATH=${PATH}:${HOME}/btfs'+str(count)+'/bin\n'
    print(command)
    chan.send(command)
    sleep(2)
    port=GetPort(count)
    command='btfs config Addresses.API /ip4/'+str(ip)+'/tcp/'+str(port+1000)+'\n'
    chan.send(command)
    sleep(2)
    command='btfs config Addresses.Gateway /ip4/'+str(ip)+'/tcp/'+str(port+4079)+'\n'
    chan.send(command)
    sleep(2)
    command='btfs config Addresses.RemoteAPI /ip4/'+str(ip)+'/tcp/'+str(port+2100)+'\n'
    chan.send(command)
    sleep(2)
    print('begin...')
    command="btfs config --json Addresses.Swarm '[\"/ip4/"+str(ip)+"/tcp/"+str(port)+"\""+",\"/ip4/"+str(ip)+"/udp/"+str(port)+"/quic\"]'"+"\n"
    print(command)
    chan.send(command)
    sleep(3)
    count+=1
