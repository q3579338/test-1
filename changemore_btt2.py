'''
Author: honus
Date: 2022-01-24 18:42:36
LastEditTime: 2022-01-24 19:26:06
LastEditors: honus
Description: 
FilePath: \test\changemore_btt2.py
'''

import xlrd
import xlwt
import os
import paramiko
import re
from time import sleep

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
    
    command='cat .btfs/config'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    print(res)
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
        return
    try:
        PeerID=re.search(PeerID, res).group(1)
    except:
        tables.write(begin, 0, ip)
        tables.write(begin, 2, 'PeerID not found')
        begin+=1
        excel.save('result.xls')
        return
    try:
        PrivKey=re.search(PrivKey, res).group(1)
    except:
        tables.write(begin, 0, ip)
        tables.write(begin, 2, 'PrivKey not found')
        begin+=1
        excel.save('result.xls')
        return
    
    tables.write(begin, 0, ip)
    tables.write(begin, 1, NO)
    tables.write(begin, 3, PeerID)
    tables.write(begin, 4, PrivKey)
    tables.write(begin, 5, Mnemonic)
    begin+=1

    Mnemonic_replace=Mnemonic_List[NO]
    PeerID_replace=PeerID_List[NO]
    PrivKey_replace=PrivKey_List[NO]

    command="sed -i 's/"+Mnemonic+"/"+Mnemonic_replace+"/' .btfs/config"
    print(command)
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    command="sed -i 's/"+PeerID+"/"+PeerID_replace+"/' .btfs/config"
    print(command)
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    command="sed -i 's/"+PrivKey.replace('/', '\/')+"/"+PrivKey_replace.replace('/', '\/')+"/' .btfs/config"
    print(command)
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()

    excel.save('result.xls')
    
if __name__ == '__main__':
    for i in range(len(ips)):
        if ips[i]:
            main(i)