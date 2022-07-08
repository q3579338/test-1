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
        print(res0)
        print(res1)
        if int(res1)==0:
            count+=1
            sleep(15)
            continue
        command='export BTFS_PATH=/root/.btfs\n'+'export PATH=${PATH}:${HOME}/btfs/bin\n'+'btfs wallet password 123456'
        stdin,stdout,stderr=client.exec_command(command)
        sleep(2)
        command='export BTFS_PATH=/root/.btfs\n'+'export PATH=${PATH}:${HOME}/btfs/bin\n'+'btfs wallet transfer THxFk5oC4QbC25ysmGBeXSSesmxyuNHK1Q '+str(res1)+' -p 123456'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print(res[0])
        sleep(15)
        count+=1
    except:
        pass