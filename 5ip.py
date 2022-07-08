'''
Author: honus
Date: 2021-09-09 08:28:38
LastEditTime: 2021-10-11 20:36:33
LastEditors: honus
Description: 添加5ip在一台服务器，前五个按照ip+port修改 后面的用第一个ip+(port+n)
FilePath: /test/5ip.py
'''

import paramiko
import os,re
from time import sleep

#1 只添加ip
#2 添加ip，修改配置文件ip+port
mode='2'

#获取5ip
command='curl ifconfig.me'
ip=os.popen(command).readlines()
wip=ip[0]
ip=ip[0].split('.')
lis=[]
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+1))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+2))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+3))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+4))
print(lis)

def GetIP(number,lis):
    if number==1:
        ip=lis[0]
    elif number==2:
        ip=lis[1]
    elif number==3:
        ip=lis[2]
    elif number==4:
        ip=lis[3]
    elif number==5:
        ip=lis[4]
    else:
        ip=lis[0]
    return ip

def GetPort(count):
    if count<=5:
        return 4001
    else:
        return 4001+count
#获取网卡名称
command="cat /proc/net/dev | awk '{i++; if(i>2){print $1}}' | sed 's/^[\t]*//g' | sed 's/[:]*$//g'"
net=[i.strip() for i in os.popen(command).readlines()]
for i in net:
    command='ifconfig '+i
    if wip in ''.join(os.popen(command).readlines()):
        nc=i
print(nc)

#检查是否添加配置文件
for i in lis:
    command='ip address add '+i+' dev '+str(nc)
    print(command)
    result=os.popen(command)
    sleep(1)

#修改配置文件
if mode=='2':
    command='ls -a'
    res=os.popen(command).readlines()
    oldport=4001
    maxnumber=0
    for data in res:
        geshu=data.find('btfs')
        shu=data.replace('.btfs','').replace('btfs','').replace('\n','')
        if geshu!=-1:
            if shu=='':
                shu=0
            else:
                shu=int(shu)
            if (shu > maxnumber):
                maxnumber=shu
    print(maxnumber)

    suc=False
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
        print('con fail')

    count=1
    while count<=maxnumber:
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
        ip=GetIP(count,lis)
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
