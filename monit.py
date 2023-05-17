'''
Author: honus
Date: 2022-03-15 20:48:58
LastEditTime: 2022-03-19 15:39:35
LastEditors: honus
Description: 
FilePath: \test\monit.py
'''
import os
import time

#MB
MaxSwap = 512

MaxNum = -1

def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def GetSwapUsed():
    command='free -m'
    res=os.popen(command).readlines()[2].split()
    return int(res[2])

def RestartBtfs(index):
    if index == 0:
        command0 = "export BTFS_PATH=/root/.btfs"
    else:
        command0 = "export BTFS_PATH=/root/.btfs" + str(index)

    if index == 0:
        command1 = "export PATH=${PATH}:${HOME}/btfs/bin"
    else:
        command1 = "export PATH=${PATH}:${HOME}/btfs" + str(index) + "/bin"

    if index == 0:
        command2 = "screen -dmS btfs"
    else:
        command2 = "screen -dmS btfs" + str(index)

    command3 = "btfs daemon --enable-gc --chain-id 199"

    command = command0 + ' && ' + command1 + ' && ' + command2 + ' ' + command3
    res = os.popen(command).readlines()
    time.sleep(10)

while True:
    swap = GetSwapUsed()
    print(gettime(), 'current swap:' ,swap)
    if swap >= MaxSwap:
        
        #kill screen
        for i in range(7):
            command = "screen -ls btfs|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
            os.popen(command)

        #get maxnumber
        if MaxNum == -1: 
            res = os.popen('ls').readlines()
            for index in res:
                if 'btfs' in index:
                    index = index.strip().replace('btfs', '')
                    if index.isdigit() :
                        if int(index)>MaxNum:
                            MaxNum = int(index)
        print('btfs number is : ' + str(MaxNum))

        time.sleep(5)

        #start btfs
        print('restart btfs')
        for i in range(1 , MaxNum+1):
            RestartBtfs(i)
            print(i , '/' , MaxNum)

        time.sleep(10)
        
        TryNum = 10
        while TryNum > 0:
            flag = 0
            RunList = []
            command = 'screen -ls'
            res = os.popen(command).readlines()
            for i in res:
                i=i.split('.')[-1].strip().split('\t')[0]
                #print(i)
                if 'btfs' in i and i.replace('btfs', '') != '':
                    flag += 1
                    RunList.append(int(i.replace('btfs', '').strip()))
            print('flag number :' + str(flag))
            if flag < MaxNum:
                for i in range(1 , MaxNum+1):
                    if i not in RunList:
                        RestartBtfs(i)
                        print(i , '/' , MaxNum)
            else:
                break
            TryNum -= 1
            time.sleep(10)

        print('restart btfs success')

    print('sleep time : 1800')
    time.sleep(1800)


        
        
