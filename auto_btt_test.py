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

def RunBtfs(index):
    if index == 0:
        command0 = "export BTFS_PATH=/root/.btfs"
    else:
        command0 = "export BTFS_PATH=/root/.btfs" + str(index)

    if index == 0:
        command1 = "export PATH=${PATH}:${HOME}/btfs/bin"
    else:
        command1 = "export PATH=${PATH}:${HOME}/btfs" + str(index) + "/bin"

    if index == 0:
        command2 = "screen -Sdm btfs"
    else:
        command2 = "screen -Sdm btfs" + str(index)

    command3 = 'btfs' + str(index) + "/bin/btfs daemon --enable-gc --chain-id 199"

    command = command0 + ' && ' + command1 + ' && ' + command2 + ' ' + command3
    print(command)
    res = os.popen(command).readlines()
    sleep(5)

for i in range(1 , maxnumber+1):
    RunBtfs(i)
    sleep(5)

TryNum = 10
while TryNum > 0:
    flag = 0
    RunList = []
    command = 'screen -ls btfs'
    res = os.popen(command).readlines()
    for i in res:
        i=i.split('.')[-1].strip().split('\t')[0]
        #print(i)
        if 'btfs' in i and i.replace('btfs', '') != '':
            flag += 1
            RunList.append(int(i.replace('btfs', '').strip()))
    print('flag number :' + str(flag))
    if flag < maxnumber:
        for i in range(1 , maxnumber+1):
            if i not in RunList:
                RunBtfs(i)
                print(i , '/' , maxnumber)
    else:
        break
    TryNum -= 1
