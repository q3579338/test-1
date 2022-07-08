'''
Author: honus
Date: 2022-01-20 22:03:25
LastEditTime: 2022-03-09 23:46:01
LastEditors: honus
Description: 
FilePath: \test\auto_btt_2.py
'''
import os
from time import sleep

lis=1
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

os.popen('wget https://raw.githubusercontent.com/0honus0/test/main/screen_btt_2.py')
while(lis<=maxnumber):
    print('now:'+str(lis))
    sleep(2)
    if lis>0:
        com='sed -i s/lis='+str(lis-1)+'/lis='+str(lis)+'/g /root/screen_btt_2.py'
        print(com)
        os.system(com)
    if lis==0:
        com='screen -Smd btfs python3 /root/screen_btt_2.py'
    else:
        com='screen -Smd btfs'+str(lis)+' python3 /root/screen_btt_2.py'
    print(com)
    # com='python3 /root/screen.py'
    os.system(com)
    lis+=1
    print('wait')
    #sleep(20)
    sleep(5)
