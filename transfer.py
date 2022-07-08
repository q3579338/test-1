import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy
import time

i=0
# i=input('输入开始位置:\n')
# i=int(i)
max_test=3
n=0
data=xlrd.open_workbook("D:/Study/python/data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#excel=copy(data1)
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('BttWallet')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')

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
                tables.write(n+1,0,ip_List[i])
                tables.write(n+1,1,password)
                excel.save('fail.xls')
                count=0
                i=i+1
                print('连接失败，开始下一个')
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")
        try:
            command='apt -y install wget'
            stdin , stdout, stderr=client.exec_command(command)
            command='wget https://raw.githubusercontent.com/0honus0/test/master/run.py'
            stdin , stdout, stderr=client.exec_command(command)
            command="sed -i 's/INPUTADDRESS/TC6rDZB7nCneTJBLH6LTWUBzJdm1BHeLXM/' run.py"
            stdin , stdout, stderr=client.exec_command(command)
            chan = client.invoke_shell()
            chan.send('screen -S zhuanzhang\n')
            sleep(1)
            chan.send('python3 run.py\n')
            sleep(2)
            print("开始后台执行。。。")
            client.close()
            count=0
            i=i+1
        except:
            client.close()
            count=0
            i=i+1
    else:
        print("连接失败")