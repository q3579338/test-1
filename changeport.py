import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
import time

ps=''
i=0
max_test=3
maxnumber=0
mingzi='znnd.xls'
begin=0

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('status')

tables=excel.get_sheet('status')
tables.write(0, 0, 'ip')
tables.write(0, 1, 'keystore')


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
                tables.write(begin+1,0,ip)
                tables.write(begin+1,2,'loginfailed')
                excel.save(mingzi)
                begin=begin+1
                count=0
                print('连接失败，开始下一个')
                break
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")
        chan=client.invoke_shell()
        command="export BTFS_PATH=/root/.btfs1\n"
        chan.send(command)
        sleep(2)
        command="export PATH=${PATH}:${HOME}/btfs1/bin\n"
        chan.send(command)
        sleep(2)
        command='btfs config Addresses.API /ip4/127.0.0.1/tcp/5001\n'
        print(command)
        chan.send(command)
        sleep(1)
        command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/8080\n'
        print(command)
        chan.send(command)
        sleep(1)
        command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/5101\n'
        print(command)
        chan.send(command)
        sleep(1)
        command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/4001\""+",\"/ip6/::/tcp/4001\""+"]'"+"\n"
        print(command)
        chan.send(command)
        sleep(1)
        print('Complete')
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    if row+1!=maxnumber:
        i=i+1