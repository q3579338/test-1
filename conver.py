import paramiko
import re,os
from time import sleep
import sys
import xlrd
import subprocess as sb
import xlwt,json

data=xlrd.open_workbook("./zhujici.xls",formatting_info=True)
table=data.sheets()[0]
zhujici_List=table.col_values(0)
row=table.nrows
print(row)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'zhujici')
tables.write(0, 1, 'btfs')
tables.write(0, 2, 'btt')

username='root'
port= 22
ip='46.4.50.59'
password=''
client=paramiko.SSHClient()
key=paramiko.AutoAddPolicy()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(ip, port, username=username, password=password,timeout=30)

count=0
while count<row:
    try:
        print('进度:'+str(count+1)+'/'+str(row))
        zhujici=zhujici_List[count]
        print(zhujici)
        command='export BTFS_PATH=/root/.btfs\n'+'export PATH=${PATH}:${HOME}/btfs/bin\n'+'btfs wallet import -m '+'\''+zhujici+'\''
        stdin,stdout,stderr=client.exec_command(command)
        sleep(3)
        command='export BTFS_PATH=/root/.btfs\n'+'export PATH=${PATH}:${HOME}/btfs/bin\n'+'btfs wallet balance'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()[0].strip()
        res=json.loads(res)
        res0=res['BtfsWalletBalance']
        res1=res['BttWalletBalance']
        tables.write(count+1,0,zhujici)
        tables.write(count+1,1,res0)
        tables.write(count+1,2,res1)
        print(res0)
        print(res1)
        if int(res0)<1000000000:
            count+=1
            excel.save('result.xls')
            sleep(15)
            continue
        command='export BTFS_PATH=/root/.btfs\n'+'export PATH=${PATH}:${HOME}/btfs/bin\n'+'btfs wallet password 123456'
        stdin,stdout,stderr=client.exec_command(command)
        sleep(2)
        command='export BTFS_PATH=/root/.btfs\n'+'export PATH=${PATH}:${HOME}/btfs/bin\n'+'btfs wallet withdraw '+str(res0)+' -p 123456'
        stdin,stdout,stderr=client.exec_command(command)
        sleep(15)
        excel.save('result.xls')
        count+=1
    except:
        count+=1