'''
Author: honus
Date: 2022-03-09 21:04:21
LastEditTime: 2022-03-15 21:45:11
LastEditors: honus
Description:  1-1 
FilePath: \test\backup_restore.py
'''
import os
import paramiko
import xlrd
import xlwt
import logging
from multiprocessing import Pool
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('backup_restore')
logger.setLevel(logging.INFO)

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

OldIps = table.col_values(0)[1:]
OldPasswords = table.col_values(1)[1:]

NewIps = table.col_values(2)[1:]
NewPasswords = table.col_values(3)[1:]


def connect(ip,password):
    try:
        client=paramiko.SSHClient()
        key=paramiko.AutoAddPolicy()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port= 22, username='root', password=password,timeout=30)
        logger.info(ip+" connect success")
        return client
    except:
        return False

def back(OldIp , OldPassword):
    client = connect(OldIp , OldPassword)
    if client:
        command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'tar -cvf btt.tar btfs .btfs*'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
    if res == []:
        logger.warning(OldIp + " backup failed")
        return False
    
    command = 'md5sum btt.tar'
    stdin, stdout, stderr = client.exec_command(command)
    md5 = stdout.readlines()

    command = "screen -Smd server python3 -m http.server 55555"
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.readlines()
    return md5
    
def restore(OldIp , NewIp , NewPassword , md5):
    client = connect(NewIp , NewPassword)
    if client:
        command = 'curl -O http://'+str(OldIp)+':55555/btt.tar'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'md5sum btt.tar'
        stdin, stdout, stderr = client.exec_command(command)
        md5_new = stdout.readlines()
        if md5_new != md5:
            logger.warning(NewIp + " download failed")
            return False
        logger.info(NewIp + " download success")
        command = 'tar -xvf btt.tar'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        logger.info(NewIp + " tar success")

        command = 'ls -a'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()

        MaxNumber = 0
        for k in res:
            if 'btfs' in k:
                k = k.replace('btfs', '').replace('.','').strip()
                if k!='' and int(k)>MaxNumber:
                    MaxNumber = int(k)

        op = ''
        for i in range(1,MaxNumber+1):
            op += 'btfs'+str(i)+' '

        command = 'echo '+op+'|'+'xargs -n1 cp -r btfs'
        #logging.info(command)
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()

        logger.info(NewIp + " restore success")

        # command = 'rm -rf btt.tar'
        # stdin, stdout, stderr = client.exec_command(command)
        # res = stdout.readlines()
        command = 'rm -rf auto_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'rm -rf screen_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'curl -O https://raw.githubusercontent.com/0honus0/test/main/auto_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = "screen -Smd run python3 auto_btt_test.py"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        logger.info('***************************************')
        logger.info(NewIp + " start running,Over")
        logger.info('***************************************')
        return True


def main(no):
    OldIp = OldIps[no]
    OldPassword = OldPasswords[no]
    NewIp = NewIps[no]
    NewPassword = NewPasswords[no]

    res =  back(OldIp, OldPassword)
    if not res:
        logger.warning(str(no) +' : '+ OldIp + " backup failed")
    else:
        logger.info(str(no) +' : '+ OldIp + " backup success")
        logger.info(str(no) +' : '+ NewIp + " begin restore")
        

    res =  restore(OldIp, NewIp, NewPassword, res)
    if res:
        logger.info(str(no) +' : '+ NewIp + " restore success")
    else:
        logger.warning(str(no) +' : '+ NewIp + " restore failed")

if __name__ == '__main__':
    OldIps = [key for key in OldIps if key != '']
    pool = Pool(32)
    for i in range(len(OldIps)):
        pool.apply_async(main, (i,))
    pool.close()
    pool.join()

