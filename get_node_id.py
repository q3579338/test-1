'''
Author: honus
Date: 2022-05-22 10:41:46
LastEditTime: 2022-05-22 13:28:36
LastEditors: honus
Description: 查询节点ID
FilePath: /test/get_node_id.py
'''
import os
import paramiko
import xlrd
import xlwt
from multiprocessing import Pool

Ip       = ""
PassWord = ""

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
Ids = table.col_values(0)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 1, 'Id')
tables.write(0, 2, 'Connect')

flag = 1

def connect(ip,password):
    MaxTestNum = 3
    while True:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            print(f"{ip} connect success")
            return client
        except:
            if MaxTestNum > 0:
                MaxTestNum -= 1
            else:
                return False

def get_node_id(Ip , PassWord):
    global flag
    client = connect(Ip , PassWord)
    if client:
        for Id in Ids:
            command1 = f"export BTFS_PATH=/root/.btfs1"
            command2 = f"export PATH=${{PATH}}:${{HOME}}/btfs1/bin"
            padding  = "&&"
            command0 = f"{command1} {padding} {command2} {padding}"

            command = f"btfs swarm connect /btfs/{Id} && btfs swarm peers | grep {Id}"
            command = f"{command0} {command}"
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            print(res)
            tables.write(flag , 0 , Id)
            if res:
                tables.write(flag , 1 , res[1].split())
            else:
                tables.write(flag , 2 , 'Get Failed')
            flag+=1
            excel.save('Get_Id.xls')
        client.close()
    else:
        return False

if __name__ == '__main__':
    Ids = [k for k in Ids if k != '']

    get_node_id(Ip , PassWord)

    #excel.save('result.xls')