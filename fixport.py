'''
Author: honus
Date: 2021-10-01 14:25:16
LastEditTime: 2021-10-02 13:59:53
LastEditors: honus
Description: 修复一些vps api端口冲突问题， api：5000+  Gateway: 8080+ Remote: 6101+
FilePath: /test/fixport.py
'''

import json
import os
from time import sleep
import re

command='ls -a'
res=os.popen(command).readlines()
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

API_port=5001
Gateway_port=8080
RemoteAPI_port=6101
for con in range(1,maxnumber):
    try:
        if con==1:
            os.environ['BTFS_PATH'] = '/root/.btfs1/'
            os.environ['PATH'] = '${PATH}:${HOME}/btfs1/bin'
            command="btfs/bin/btfs config Addresses.API /ip4/127.0.0.1/tcp/"+str(API_port)
            print(command)
            res=os.popen(command)
            sleep(1)
            command="btfs/bin/btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/"+str(Gateway_port)
            print(command)
            res=os.popen(command)
            sleep(1)
            command="btfs/bin/btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/"+str(RemoteAPI_port)
            print(command)
            res=os.popen(command)
            sleep(1)
        else:
            os.environ['BTFS_PATH'] = '/root/.btfs'+str(con)+'/'
            os.environ['PATH'] = '${PATH}:${HOME}/btfs'+str(con)+'/bin'
            command="btfs/bin/btfs config Addresses.API /ip4/127.0.0.1/tcp/"+str(API_port+con)
            print(command)
            res=os.popen(command)
            sleep(1)
            command="btfs/bin/btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/"+str(Gateway_port+con)
            print(command)
            res=os.popen(command)
            sleep(1)
            command="btfs/bin/btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/"+str(RemoteAPI_port+con)
            print(command)
            res=os.popen(command)
            sleep(1)
    except:
        continue
