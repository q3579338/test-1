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
        command="ss-tproxy stop"
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='service systemd-resolved restart'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('Complete')
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    i=i+1
