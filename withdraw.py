import os
import paramiko
import xlrd
import xlwt
import logging
import re

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

Ips = table.col_values(0)
Passwords = table.col_values(1)

flag = 1
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'Ip')
tables.write(0, 1, 'Number')
tables.write(0, 2, 'Status')

def connect(ip,password):
    MaxTestNum = 3
    while True:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            print(ip+" connect success")
            return client
        except:
            if MaxTestNum > 0:
                MaxTestNum -= 1
            else:
                return False

def main(no):
    ret = []
    ip = Ips[no]
    password = Passwords[no]

    client = connect(ip,password)
    if not client:
        return False , (ip , 0 , 'connect failed')
    

    command='ls'
    stdin,stdout,stderr=client.exec_command(command)
    res=stdout.readlines()
    maxnumber=0
    for data in res:
        geshu=data.find('btfs')
        shu=data.replace('btfs','').replace('\n','')
        if geshu!=-1:
            if shu=='':
                shu=0
            else:
                shu=int(shu)
            if shu > maxnumber:
                maxnumber=shu
    #print(maxnumber)

    if maxnumber == 0:
        pass
    else:
        pat = '"API": "\/ip4\/127.0.0.1\/tcp\/(\d+)"'
        for i in range(1,maxnumber + 1):
            print(ip , i , '/' , maxnumber)
            command='cat .btfs' + str(i) + '/config'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.read().decode('utf-8')
            try:
                api = re.search(pat, res).group(1)
                command = 'curl -s https://raw.githubusercontent.com/bittorrent/go-btfs/master/scripts/batch_cash.sh | bash -s 127.0.0.1:' + str(api)
                stdin,stdout,stderr=client.exec_command(command)
                res=stdout.read().decode('utf-8')
                if 'Success, all tasks completed!' not in res:
                    ret.append((ip , i , 'run failed')) 
            except:
                print( ip , i+1 , 'error')
                ret.append((ip , i, 'error'))
    return True , ret

Ips = [k for k in Ips if k != '']
Passwords = [k for k in Passwords if k != '']

for i in range(0 , len(Ips)):
    status , tmp = main(i)
    if status:
        for j in tmp:
            tables.write(flag, 0, j[0])
            tables.write(flag, 1, j[1])
            tables.write(flag, 2, j[2])
            flag += 1
    else:
        tables.write(flag, 0, tmp[0])
        tables.write(flag, 1, tmp[1])
        tables.write(flag, 2, tmp[2])
        flag += 1
    excel.save('./result.xls')

# for i in all_data:
#     status , tmp = i.get()
#     if status:
#         for j in tmp:
#             tables.write(flag, 0, j[0])
#             tables.write(flag, 1, j[1])
#             tables.write(flag, 2, j[2])
#             flag += 1
#     else:
#         tables.write(flag, 0, tmp[0])
#         tables.write(flag, 1, tmp[1])
#         tables.write(flag, 2, tmp[2])
#         flag += 1
#     excel.save('./result.xls')
