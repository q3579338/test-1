'''
Author: honus
Date: 2022-07-08 09:51:32
LastEditTime: 2022-07-08 10:46:12
LastEditors: honus
Description: 
FilePath: /test/changepassword.py
'''
import os
import paramiko
import xlrd
import xlwt
from multiprocessing import Pool
from time import sleep

PASSWORD = ""

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

Ips = table.col_values(0)
Passwords = table.col_values(1)

flag = 1
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'status')

def connect(ip,password):
    try:
        client=paramiko.SSHClient()
        key=paramiko.AutoAddPolicy()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port= 22, username='root', password=password,timeout=30)
        print(f"{ip} 连接成功")
        return client
    except:
        return False

def changepassword(client):
    global PASSWORD

    command = """
    echo root:""" + str(PASSWORD) +""" |sudo chpasswd root
    """

    # sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config;
    # sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config;
    # sudo service sshd restart

    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.readlines()
    client.close()
    print("执行成功")
    return True

def main(no):
    global flag

    ip = Ips[no]
    password = Passwords[no]
    client = connect(ip, password)

    if not client:
        tables.write(flag , 0 , ip)
        tables.write(flag , 1 , password)
        tables.write(flag , 2 , 'connect failed')
        flag+=1
        return False

    res = changepassword(client)
    return res

    
if __name__ == '__main__':
    Ips = [key for key in Ips if key != '']
    Passwords = [key for key in Passwords if key != '']

    pool = Pool(8)
    result = []
    for i in range(len(Ips)):
        q = pool.apply_async(main, (i,))
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


