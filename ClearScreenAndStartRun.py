'''
Author: honus
Date: 2022-03-19 18:57:26
LastEditTime: 2022-03-19 21:39:35
LastEditors: honus
Description: 
FilePath: \test\ClearScreenAndStartRun.py
'''
import xlrd
from multiprocessing import Pool
import paramiko
from time import sleep
data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

Ips = table.col_values(0)[1:]
Passwords = table.col_values(1)[1:]


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
                print(ip+" connect failed")
                return False

def main(i):
    ip = Ips[i]
    password = Passwords[i]
    client = connect(ip,password)
    if client:
        for k in range(0,6):
            command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            sleep(1)
        command = 'rm -rf wget-log.* && rm -rf auto_btt_test.py && rm -rf monit.py && rm -rf screen_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'wget https://raw.githubusercontent.com/0honus0/test/main/auto_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'screen -Sdm run2.1T python3 auto_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'wget https://raw.githubusercontent.com/0honus0/test/main/monit.py'
        stdin , stdout , stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'screen -Sdm monit python3 monit.py'
        stdin , stdout , stderr = client.exec_command(command)
        res = stdout.readlines()
        client.close() 
        print(ip+" run success")   

if __name__ == "__main__":
    Ips = [k for k in Ips if k != '']
    pool = Pool(processes=16)
    for i in range(len(Ips)):
        pool.apply_async(main,args=(i,))
    pool.close()
    pool.join()
    print("All subprocesses done.")
    
