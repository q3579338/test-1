import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
import time

i=0
max_test=3
begin=0
data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows


while row > i:
    count=0
    success=False
    while count < max_test and not success:
        try:
            username='root'
            port= 22
            ip=ip_List[i]
            password=password_List[i]
            print(ip)
            print(password)
            print('当前在第'+str(i+1)+'个')
            print('尝试第'+str(count+1)+'次登陆')
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, username=username, password=password,timeout=30)
            success = True
        except:
            if count == max_test-1:
                print('连接失败，开始下一个')
                break
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")
        command='ls'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        maxnum=0
        for data in res:
            geshu=data.find('btfs')
            shu=data.replace('btfs','').replace('\n','')
            if geshu!=-1:
                if shu=='':
                    shu=0
                else:
                    shu=int(shu)
                if shu > maxnum:
                    maxnum=shu
        value=0
        for value in range(1,maxnum+1):
            print(value)
            print("进度: "+str(value)+'/'+str(maxnum))
            chan=client.invoke_shell()
            if value==0:
                command='export BTFS_PATH=/root/.btfs\n'
            else:
                command='export BTFS_PATH=/root/.btfs'+str(value)+'\n'
            chan.send(command)
            sleep(2)
            if value==0:
                command='export PATH=${PATH}:${HOME}/btfs/bin\n'
            else:
                command='export PATH=${PATH}:${HOME}/btfs'+str(value)+'/bin\n'
            chan.send(command)
            sleep(2)
            command='btfs config --json Bootstrap []\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/54.255.27.251/tcp/4001/p2p/QmURPwdLYesWUDB66EGXvDvwcyV44rVRqV2iGNqKN24eVu\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/13.213.254.73/tcp/4001/p2p/QmX7RZXh27AX8iv2BKLGMgPBiuUpEy8p4LFXgtXAfaZDn9\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/52.221.82.136/tcp/4001/p2p/QmYqCq3PasrzLr3PxtLo5D6spEAJ836W9Re9Eo4zUou45U\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/3.1.76.240/tcp/4001/p2p/16Uiu2HAmQfh6CYSWG1MM1DnzJ9duM8jxqn6vxNbjGBsmzc3kkctp\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/34.213.53.108/tcp/4001/p2p/QmWm3vBCRuZcJMUT9jDZysoYBb66aokmSReX26UaMk8qq5\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/35.161.203.220/tcp/4001/p2p/QmWJWGxKKaqZUW4xga2BCzT5FBtYDL8Cc5Q5jywd6xPt1g\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/35.84.213.199/tcp/4001/p2p/QmbVFdiNkvxtc7Nni7yBWAgtHg8MuyhaZ5mDaYR2ZrhhvN\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/35.84.151.38/tcp/4001/p2p/QmQVQBsM7uoJy8hATjTm51uSAkx2y3iGLhSwA6LWLa7iQJ\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/3.66.57.90/tcp/4001/p2p/16Uiu2HAmFT6NXQkzDZXHxuFC4qFt6D1ALf57AkJV9U54HoafX7FX\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/3.69.104.217/tcp/4001/p2p/16Uiu2HAm2v2NBTLYmzVnLJoNbLCmdn29Gv8qLixHCJNeE81rUUYe\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/3.126.224.22/tcp/4001/p2p/16Uiu2HAmNngtNogFpcAUdc6wdSDmb8ZZQjjoDDWaatBXW1rHsYpu\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/35.158.193.90/tcp/4001/p2p/16Uiu2HAmLY4kyhMuoBntyXSt2YssZCHjefHEAXrYVc6acB7KEBh3\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/13.232.5.9/tcp/4001/p2p/16Uiu2HAmSkFDwHU3snrYD2ib5wWeKcsuFMZWEPt31z5YVJ8ktw1p\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/3.7.220.224/tcp/4001/p2p/16Uiu2HAmRVtFaXksAqb8W4Fyr8g5jkggeGDFdVcp8dQ724NMvpcR\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/3.109.125.91/tcp/4001/p2p/16Uiu2HAkzggX1jKwc1xen5qNPQ5RKNkXQqmH2PYAKGd8JZ15YQmK\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/65.1.217.86/tcp/4001/p2p/16Uiu2HAmGwDdvK4jAi1Ahga3zkiuW6HFZKKFNWtqVUFXvaSCNjdg\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/15.184.174.48/tcp/4001/p2p/16Uiu2HAm6Bkxj81JQxa67aja7UWznjTgzAAVzPAqZMVD6oGpw7ST\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/15.184.108.65/tcp/4001/p2p/16Uiu2HAkzRyGYEba2B3SBXdwp328LNFhRG4qhJVZrN6tsJK5KKu5\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/15.184.96.102/tcp/4001/p2p/16Uiu2HAmFVWTvouWpQTRjMb4bUaidfLzsH2RVogcGHb6RwvPSxuT\n'
            chan.send(command)
            sleep(1)
            command='btfs bootstrap add /ip4/15.184.66.135/tcp/4001/p2p/16Uiu2HAmBQcXzrgo9MVD8xZwt4CrLzPRK1yKAVM7eY9GhXMJYHmC\n'
            chan.send(command)
            sleep(1)
        print('Complete')
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    i=i+1
