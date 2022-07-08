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

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List

#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('login')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'login')

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
                tables.write(i+1,0,ip_List[i])
                tables.write(i+1,1,password)
                tables.write(i+1,2,'loginfailed')
                excel.save('delay.xls')
                count=0
                i=i+1
                print('连接失败，开始下一个')
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")
        command='rm -rf auto.py'
        stdin,stdout,stderr=client.exec_command(command)
        sleep(1)
        command='rm -rf screen.py'
        stdin,stdout,stderr=client.exec_command(command)
        sleep(1)
        command='wget https://raw.githubusercontent.com/0honus0/test/main/auto.py'
        stdin,stdout,stderr=client.exec_command(command)
        sleep(1)
        chan = client.invoke_shell()
        com='screen -S run\n'
        chan.send(com)
        sleep(1)
        com='python3 auto.py\n'
        chan.send(com)
        sleep(2)
        count=0
        i=i+1
    else:
        print("连接失败")
