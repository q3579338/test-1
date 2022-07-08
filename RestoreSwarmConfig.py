'''
Author: honus
Date: 2022-03-19 21:27:49
LastEditTime: 2022-03-19 21:36:46
LastEditors: honus
Description: 
FilePath: \test\RestoreSwarmConfig.py
'''
import os
from time import sleep
maxnumber=0
res=os.popen('ls')
for data in res:
    geshu=data.find('btfs')
    shu=data.replace('btfs','').replace('\n','')
    if geshu!=-1:
        if shu=='':
            shu=0
        else:
            shu=int(shu)
        if shu > maxnumber:
            maxnumber=shu
print(maxnumber)

command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
for i in range(6):
    os.popen(command)
    sleep(1)

for i in range(maxnumber+1):
    if i == 0:
        command0 = "export BTFS_PATH=/root/.btfs"
    else:
        command0 = "export BTFS_PATH=/root/.btfs" + str(i)

    if i == 0:
        command1 = "export PATH=${PATH}:${HOME}/btfs/bin"
    else:
        command1 = "export PATH=${PATH}:${HOME}/btfs" + str(i) + "/bin"

    port = 4002 + i
    command2 = "btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(port)+"\""+",\"/ip6/::/tcp/"+str(port)+"\""+"]'"+"\n"


    command = command0 + ' && ' + command1 + ' && ' + command2
    print(command)
    res = os.popen(command).readlines()
    sleep(5)
