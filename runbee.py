import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt

i=0
max_test=3
begin=0

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)
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
            #print(password)
            print('当前在第'+str(i+1)+'个')
            #print('尝试第'+str(count+1)+'次登陆')
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, username=username, password=password,timeout=30)
            success = True
        except:
            if count == max_test-1:
                count=0
                i=i+1
                print('连接失败，开始下一个')
            else:
                print('登陆失败，尝试重新登陆')
                count =count+1
    if success:
        print('登陆成功')
        command="sed -i 's/# swap-endpoint: http:\/\/localhost:8545/swap-endpoint: https:\/\/goerli.infura.io\/v3\/cd8135ee2e07404ab7fd85b862c01f59/' /etc/bee/bee.yaml"
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        command='sudo chown -R bee:bee /var/lib/bee'
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        command='chown bee-clef /var/lib/bee-clef/clef.ipc'
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        command='chgrp bee-clef /var/lib/bee-clef/clef.ipc'
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        command='sudo systemctl start bee'
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        print('运行成功')
    else:
        print("连接失败")
    max_test=3
    i=i+1
    success=False

#Goerli
#https://goerli.infura.io/v3/cd8135ee2e07404ab7fd85b862c01f59