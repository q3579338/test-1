import paramiko
import re,os
from time import sleep
import sys
import xlrd
import subprocess as sb
import xlwt

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('Key')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'name')
tables.write(0, 2, 'status')

i=0
max_test=3
while row > i:
    count=0
    success=False
    while count < max_test and not success:
        try:
            while ip_List[i+1]=='' or password_List[i+1]=='':
                print('完成')
                sys.exit(0)
        except:
            pass
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
                count=0
                i=i+1
                print('连接失败，开始下一个')
            else:
                print('登陆失败，尝试重新登陆')
                count =count+1
    if success:
        name=''
        command='ls /var/lib/bee-clef/keystore'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        if res==[]:
            print('内容为空')
            tables.write(i+1, 0, ip)
            tables.write(i+1, 2, 'failed')
            excel.save('key-store.xls')
            continue
        name=res[0].strip('\n')
        print(name)
        command='cat /var/lib/bee-clef/keystore/'+str(name)
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print(res)
        os.makedirs(ip)
        with open('./'+ip+'/'+name,'w') as f:
            f.write(res[0].strip('\n'))
        command='cat /var/lib/bee-clef/password'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print(res)
        with open('./'+ip+'/password','w') as f:
            f.write(res[0].strip('\n'))
        tables.write(i+1, 0, ip)
        tables.write(i+1, 1, name)
        tables.write(i+1, 2, 'success')
        excel.save('key-store.xls')
    else:
        print("连接失败")
    max=0
    i=i+1
    success=False