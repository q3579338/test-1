import os
from time import sleep
import time
import re
def gettime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

while(True):
    command='free -m'
    res=os.popen(command).readlines()[2].split()
    print('swap used:'+str(res[2])+'/'+str(res[1]))
    if int(res[2])>1024:
        print(gettime())
        print('begin del screen...')
        command='ls /root'
        res=os.popen(command).readlines()
        maxnumber=0
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
        command='screen -S run -X quit'
        os.popen(command)
        command='screen -S btfs -X quit'
        os.popen(command)
        for i in range(1,maxnumber+1):
            command='screen -S btfs'+str(i)+'  -X quit'
            os.popen(command)
        print('completed...')
        print('two...')
        try:
            for i in range(1,maxnumber+1):
                duankou=''
                command='cat .btfs'+str(i)+'/config'
                print(command)
                res=os.popen(command).readlines()
                duankou=''
                for data in res:
                    pat='\"API\": \"/ip4/127.0.0.1/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou=re.search(pat,data).group()
                        duankou=duankou[27:len(data)-1]
                print(duankou)
                port=duankou
                command='netstat -nap | grep '+str(port)
                res=os.popen(command).readlines()
                for k in res:
                    k=k.split()
                    k=k[6]
                    pat='\d{1,5}'
                    try:
                        pid=re.search(pat,k).group()
                        command='kill -9 '+str(pid)
                        os.system(command)
                        print('kill pid:'+str(pid))
                    except:
                        continue
                print('port '+str(port+i)+' free')
        except:
            pass
        print('begin reboot btfs...')
        command='rm -rf screen_btt_2.py'
        os.system(command)
        command='rm -rf auto_btt_2.py'
        os.system(command)
        command='rm -rf wget-log'
        os.system(command)
        command='wget https://raw.githubusercontent.com/0honus0/test/main/auto_btt_2.py'
        os.system(command)
        sleep(60)
        os.system('screen -dmS run python3 /root/auto_btt_2.py')
        print('rebooting...')
        count=3600
        while count>0:
            sleep(1)
            count=count-1
            print('\r' + 'sleeping:'+str(3600-count)+'/'+str(3600), end='', flush=True)
    else:
        print(gettime())
        print("normal")
        count=3600
        while count>0:
            sleep(1)
            count=count-1
            print('\r' + 'sleeping:'+str(3600-count)+'/'+str(3600), end='', flush=True)
