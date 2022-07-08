import os
import paramiko
import xlrd
import xlwt
from multiprocessing import Pool

n = 8

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

Ips = table.col_values(0)
Passwords = table.col_values(1)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'Ip')
tables.write(0, 1, 'Password')
tables.write(0, 2, 'Status')

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

def delfile(Ip , PassWord , Number):
    client = connect(Ip , PassWord)
    if client:
        Name = ''
        for i in range(1 , Number + 1):
            Name += f"btfs{i} .btfs{i} "
            print(Name)
        command = 'rm -rf ' + Name
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        client.close()
        return True
    else:
        return False

if __name__ == '__main__':
    Ips = [key for key in Ips if key != '']
    Passwords = [key for key in Passwords if key != '']

    pool = Pool(16)
    result = []
    for i in range(len(Ips)):
        q = pool.apply_async(delfile, (Ips[i],Passwords[i],n))
        result.append(q)
    pool.close()
    pool.join()

    for i in range(len(result)):
        tables.write(i+1, 0, Ips[i])
        tables.write(i+1, 1, Passwords[i])
        if result[i].get() == True:
            tables.write(i+1, 2, 'Success')
        else:
            tables.write(i+1, 2, 'Failed')
    excel.save('result.xls')