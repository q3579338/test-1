'''
Author: honus
Date: 2022-01-24 18:42:36
LastEditTime: 2022-01-24 19:43:34
LastEditors: honus
Description: 
FilePath: \test\changemore_btt2_128.py
'''

import xlrd
import xlwt
import os
import paramiko
import re
from time import sleep

max=128

data=xlrd.open_workbook('./data.xls',formatting_info=True)
table=data.sheets()[0]
ips=table.col_values(0)
passwords=table.col_values(1)
Mnemonic_List=table.col_values(2)
PeerID_List=table.col_values(3)
PrivKey_List=table.col_values(4)

row=table.nrows

excel=xlwt.Workbook(encoding='utf-8')
tables=excel.add_sheet('result')
tables=excel.get_sheet(0)

tables.write(0, 0, 'ip')
tables.write(0, 1, 'number')
tables.write(0, 2, 'failed')
tables.write(0, 3, 'PeerID')
tables.write(0, 4, 'PrivKey')
tables.write(0, 5 ,'Mnemonic')

begin=1

def main(NO):
    global excel
    global begin
    global max

    ip=ips[NO]
    password=passwords[NO]
    try_number=3
    while try_number>0:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            print(ip+" 连接成功")
            break
        except:
            try_number-=1
    if try_number==0:
        print("连接失败")
        tables.write(begin, 0, ip)
        tables.write(begin, 2, 'login failed')
        begin+=1
        excel.save('./result.xls')
        return
    
    while max > 0 :
        no=129-max
        max-=1
        print(ip+" "+str(no)+'/128')

        #change HostRepairEnabled to true
        chan = client.invoke_shell()
        command = 'export BTFS_PATH=/root/.btfs'+str(no)+'\n'
        chan.send(command)
        sleep(1)
        command = 'export PATH=${PATH}:${HOME}/btfs'+str(no)+'/bin\n'
        chan.send(command)
        sleep(1)
        command = 'btfs config --json Experimental.HostRepairEnabled true\n'
        chan.send(command)
        sleep(1)

        command='cat .btfs'+str(no)+'/config'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.read().decode()
        #print(res)
        PeerID='\"PeerID\": \"([a-zA-Z0-9|\+]+)\"'
        PrivKey='\"PrivKey\": \"([a-zA-Z0-9|\+|/]+)\"'
        Mnemonic='\"Mnemonic\": \"([a-zA-Z0-9| ]+)\"'

        try:
            Mnemonic=re.search(Mnemonic, res).group(1)
        except:
            tables.write(begin, 0, ip)
            tables.write(begin, 2, 'Mnemonic not found')
            begin+=1
            excel.save('result.xls')
            continue
        try:
            PeerID=re.search(PeerID, res).group(1)
        except:
            tables.write(begin, 0, ip)
            tables.write(begin, 2, 'PeerID not found')
            begin+=1
            excel.save('result.xls')
            continue
        try:
            PrivKey=re.search(PrivKey, res).group(1)
        except:
            tables.write(begin, 0, ip)
            tables.write(begin, 2, 'PrivKey not found')
            begin+=1
            excel.save('result.xls')
            continue
        
        tables.write(begin, 0, ip)
        tables.write(begin, 1, no)
        tables.write(begin, 3, PeerID)
        tables.write(begin, 4, PrivKey)
        tables.write(begin, 5, Mnemonic)
        begin+=1

        Mnemonic_replace=Mnemonic_List[NO*128+no-1]
        PeerID_replace=PeerID_List[NO*128+no-1]
        PrivKey_replace=PrivKey_List[NO*128+no-1]

        command="sed -i 's/"+Mnemonic+"/"+Mnemonic_replace+"/' .btfs"+str(no)+"/config"
        #print(command)
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.read().decode()
        command="sed -i 's/"+PeerID+"/"+PeerID_replace+"/' .btfs"+str(no)+"/config"
        #print(command)
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.read().decode()
        command="sed -i 's/"+PrivKey.replace('/', '\/')+"/"+PrivKey_replace.replace('/', '\/')+"/' .btfs"+str(no)+"/config"
        #print(command)
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.read().decode()

        excel.save('result.xls')
    
if __name__ == '__main__':
    for i in range(len(ips)):
        if ips[i]:
            main(i)