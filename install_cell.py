'''
Author: honus
Date: 2022-01-28 15:59:43
LastEditTime: 2022-01-28 16:03:04
LastEditors: honus
Description: 
FilePath: \test\install_cell.py
'''
import xlrd
import paramiko
from time import sleep
import re
from multiprocessing import Pool
import xlwt

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ips=table.col_values(0)
passwords=table.col_values(1)
count=len(ips)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'address')

def main(NO):
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
        return
    
    command='wget https://github.com/Cell-chain/wiki/releases/download/v0.4.0/cell && chmod +x ./cell'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    command='./cell zkp --params'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    command='./cell key generate'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    chan = client.invoke_shell()
    command='export PATH=${PATH}:${HOME}/btfs/bin'
    chan.send(command+'\n')
    sleep(1)
    command='btfs init -p storage-host-testnet'
    chan.send(command+'\n')
    sleep(1)
    command='btfs daemon --chain-id 1029'
    chan.send(command+'\n')
    sleep(1)
    res=chan.recv(2048).decode()
    Bttc=re.search('the address of Bttc format is:  ([A-Za-z0-9]+)',res).group(1)
    print(ip+' install success,Address: '+Bttc)
    chan.close()
    client.close()
    return ip,Bttc

if __name__ == '__main__':
    p=Pool(4)
    result=[]
    for i in range(count):
        res=p.apply_async(main,args=[i])
        print('第',str(i+1),'个进程启动.。。')
        result.append(res)
    p.close()
    p.join()
    index=1
    for value in result:
        value=value.get()
        #print(value)
        tables.write(index , 0, value[0])
        tables.write(index , 1, value[1])
        index+=1
    excel.save('./result.xls')
    print('所有进程运行完成')






