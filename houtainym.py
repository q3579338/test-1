import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy
import time

i=0
max_test=3
begin=0

#添加ipv6
#ifconfig eno1 inet6 add 2a01:4f9:4b:14ce::3/64 up
#删除ipv6
#ifconfig enp4s0f3 inet6 del 8888::a99/96

time='houtainym'
data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('nym')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'status')

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
                tables.write(begin+1,1,password)
                tables.write(begin+1,2,'loginfailed')
                mingzi=time+".xls"
                print(mingzi)
                excel.save(mingzi)
                i=i+1
                begin=begin+1
                count=0
                print('连接失败，开始下一个')
                break
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")

        command='ls'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        lis=0
        for data in res:
            #print(data)
            geshu=data.find('nym-mixnode_linux_x86_64')
            shu=data.replace('nym-mixnode_linux_x86_64','').replace('\n','')
            if geshu!=-1:
                if shu=='':
                    shu=0
                else:
                    shu=int(shu.replace('_',''))
                if shu > lis:
                    lis=shu
        #print(lis)

        houtai=0
        while  houtai<=lis:
            try:
                print('进度:'+str(houtai)+'/'+str(lis))
                chan = client.invoke_shell()
                command='screen -S nym'+str(houtai)+'\n'
                chan.send(command)
                print(command)
                sleep(2)
                if houtai==0:
                    command='./nym-mixnode_linux_x86_64 run --id nym'+str(houtai)+'\n'
                else:
                    command='./nym-mixnode_linux_x86_64_'+str(houtai)+' run --id nym'+str(houtai)+'\n'
                print(command)
                chan.send(command)
                sleep(2)
                print('开始后台运行...')
                houtai=houtai+1
            except:
                tables.write(begin+1,0,ip)
                tables.write(begin+1,1,lis)
                tables.write(begin+1,2,'runInterrupt')
                begin=begin+1
                houtai=houtai+1
                mingzi=time+".xls"
                excel.save(mingzi)
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    if row+1!=maxnumber:
        i=i+1