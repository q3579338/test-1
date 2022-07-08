import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy

i=0
max_test=3
loginfailed=1
delfailed=1

data=xlrd.open_workbook("D:/Study/python/data.xls",formatting_info=True)
data1=xlrd.open_workbook("D:/Study/python/Failed.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
excel=copy(data1)
#行数
row=table.nrows
tables=excel.get_sheet(0)
tables.write(0, 0, 'loginfailed')
tables.write(0, 1, 'delfailed')

while row > i:
    print(row)
    print(i)
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
                tables.write(loginfailed,0,ip)
                loginfailed += 1
                excel.save('Failed.xls')
                count=0
                if row > i+1:
                    print('连接失败，开始下一个')
                    i=i+1
                else:
                    print('连接失败，开始下一个')
                    sys.exit(0)
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")
        delresult=False
        test=3

        command='ls -a'
        stdin,stdout,stderr=client.exec_command(command)
        result=stdout.readlines()
        #print(result)

        while test > 0 and delresult is False:
            command='rm -rf btfs'
            stdin,stdout,stderr=client.exec_command(command)
            command='rm -rf .btfs'
            stdin,stdout,stderr=client.exec_command(command)
            command='rm -rf install.sh'
            stdin,stdout,stderr=client.exec_command(command)
            command='ls -a'
            stdin,stdout,stderr=client.exec_command(command)
            result=stdout.readlines()
            #print(result)
            flag=1
            for data in result:
                if data.find('btfs')!=-1:
                    data=data.replace('\n','')
                    if 'btfs' in data or '.btfs' in data:
                        flag=0
            if flag==1:
                delresult=True
                print('删除成功')
            else:
                print('删除失败，重试')
                test=test-1

        if delresult is False:
            tables.write(delfailed,1,ip)
            delfailed += 1
        #重启
        command='/sbin/reboot -f > /dev/null 2>&1 &'
        stdin,stdout,stderr=client.exec_command(command)
        sleep(1)
        client.close()
        print("完成")
        excel.save('Failed.xls')
        count=0
        i=i+1
    else:
        print("连接失败")

