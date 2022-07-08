import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy

i=0
max=255
max_test=3

data=xlrd.open_workbook("D:/data.xls",formatting_info=True)
data1=xlrd.open_workbook("D:/alldata.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
excel=copy(data1)
#行数
row=table.nrows

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'str')

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
            print('登陆失败，尝试重新登陆')
            sleep(1)
            count +=1
            if count == max_test:
                 break
    if success:
        print("连接成功")

        command=('cat .btfs/config')
        stdin, stdout, stderr = client.exec_command(command)
        results = stdout.readlines()
        find=False
        for data in results:
            while  data.find("Mnemonic",0,len(data))!=-1 and find==False:
                zifu=data.find("Mnemonic",0,len(data))
                find=True
                wri=data[zifu+12:len(data)-3]
                print(wri)
                tables.write(i+1, 0, ip)
                tables.write(i+1, 1, password)
                tables.write(i+1, 2, wri)

        command=('apt-get -y install screen')
        stdin, stdout, stderr = client.exec_command(command)
        sleep(10)
        #'screen -S a -d -m btfs/bin/btfs daemon\n'
        chan = client.invoke_shell()
        chan.send('export PATH=${PATH}:${HOME}/btfs/bin\n')
        sleep(2)
        chan.send('screen -S a\n')
        sleep(3)
        chan.send('btfs daemon\n')
        sleep(5)
        print("开始后台执行。。。")
        client.close()
        excel.save('alldata.xls')
        sleep(3)
        print("完成")
    else:
        print("连接失败")
        sys.exit(0)
    max=0
    i=i+1
    success=False
