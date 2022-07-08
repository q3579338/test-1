import os , re
import paramiko
import xlrd
import xlwt
import logging
from multiprocessing import Pool

count = 1

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]
Ips = table.col_values(0)[1:]
Passwords = table.col_values(1)[1:]

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')

tables=excel.get_sheet('result')
tables.write(0, 0, 'ip')
tables.write(0, 1, 'screen_count')

def connect(ip,password):
    MaxTestNum = 3
    while True:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            return client
        except:
            if MaxTestNum > 0:
                MaxTestNum -= 1
            else:
                return False

def main(no):
    print(no)
    ip = Ips[no]
    password = Passwords[no]
    client = connect(ip,password)
    screen_count = None
    if client:
        command = 'screen -ls'
        stdin , stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        if res:
            pat = '(\d+) Sockets in /run/screen/S-root'
            try:
                screen_count = re.search(pat,res[-1]).group(1)
            except:
                pass
    return ip , screen_count
    


if __name__ == '__main__':
    Ips = [k for k in Ips if k != '']
    Passwords = [k for k in Passwords if k != '']

    all_res = []
    p = Pool(32)
    for i in range(len(Ips)):
        q = p.apply_async(main, args=(i,))
        all_res.append(q)

    p.close()
    p.join()

    for data in all_res:
        if data.get() != None:
            tables.write(count, 0, data.get()[0])
            tables.write(count, 1, data.get()[1])
            count += 1
            excel.save('./result.xls')  