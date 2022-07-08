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
        command="wget -O cashout.sh https://gist.githubusercontent.com/ralph-pichler/3b5ccd7a5c5cd0500e6428752b37e975/raw/b40510f1172b96c21d6d20558ca1e70d26d625c4/cashout.sh && chmod +x cashout.sh"
        stdin, stdout, stderr = client.exec_command(command)
        sleep(2)
        stdout.readlines()
        command="sed -i 's/MIN_AMOUNT=10000000000000000/MIN_AMOUNT=10000/' cashout.sh"
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        command="sed -i '$a00 02 * * * root /root/cashout.sh cashout-all' /etc/crontab"
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        command="service cron reload"
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        print('运行成功')
    else:
        print("连接失败")
    max_test=3
    i=i+1
    success=False