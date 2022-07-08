'''
Author: honus
Date: 2022-01-19 16:33:54
LastEditTime: 2022-01-20 21:44:11
LastEditors: honus
Description: 批量转账
FilePath: \test\tran_btt.py
'''
import xlrd,xlwt
from multiprocessing import Pool
import os
from time import sleep
import paramiko

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ips=table.col_values(0)
passwords=table.col_values(1)
addresss=table.col_values(2)
count=len(ips)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('failed')
tables=excel.get_sheet(0)
tables.write(0, 0, 'address')

def login(ip,password):
    try_number=3
    while try_number>0:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            print(ip+" 连接成功")
            return client
        except:
            try_number-=1
    if try_number==0:
        print("连接失败")
        return

if __name__ == '__main__':
    begin=1
    for i in range(count):
        ip=ips[i]
        if not ip:
            os._exit(0)
        password=passwords[i]
        client=login(ip,password)
        if client:
            flag=5
            while flag>0:
                command='apt -y install curl'
                stdin,stdout,stderr=client.exec_command(command)
                res=stdout.read().decode()
                try:
                    address=addresss.pop()
                    while not address:
                        address=addresss.pop()
                except:
                    os._exit(0)
                command="curl 'https://trontest.com:3001/transferbttc?address="+str(address)+"&token=btt'"
                stdin,stdout,stderr=client.exec_command(command)
                res=stdout.read().decode()
                print(res)
                sleep(2)
                if '成功' in res:
                    pass
                else:
                    tables.write(begin, 0, address)
                    begin+=1
                flag-=1
            excel.save('failed.xls')
            client.close()
