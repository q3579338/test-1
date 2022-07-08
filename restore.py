'''
Author: honus
Date: 2022-03-09 21:04:21
LastEditTime: 2022-03-13 18:11:30
LastEditors: honus
Description:  8-8 64-8
FilePath: \test\restore.py
'''
import os
import paramiko
import xlrd
import xlwt
import logging
from multiprocessing import Pool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('backup_restore')

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

NewIps = table.col_values(0)[1:]
NewPasswords = table.col_values(1)[1:]
NewUrls = table.col_values(2)[1:]

def connect(ip,password):
    try:
        client=paramiko.SSHClient()
        key=paramiko.AutoAddPolicy()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port= 22, username='root', password=password,timeout=30)
        logger.info(ip+" connect success")
        return client
    except:
        logger.warning(ip+" connect failed")
        return False
 
def restore(NewIp,NewPassword , NewUrl):
    NewUrl = NewUrl.strip()
    FileName = NewUrl.split('/')[-1]
    client = connect(NewIp , NewPassword)
    if client:
        command = 'apt -y install unzip'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        logger.info(NewIp + " install unzip success")
        logger.info(NewIp + " begin download")
        command = "rm -rf "+FileName
        stdin, stdout, stderr = client.exec_command(command)
        res =   stdout.readlines()
        command = 'wget -nc '+ NewUrl
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        logger.info(NewIp + " download success")
        command = 'unzip -o' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        logger.info(NewIp + " unzip success")

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

        command = 'rm -rf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
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
    NewIp = NewIps[no]
    NewPassword = NewPasswords[no]
    NewUrl = NewUrls[no]

    res =  restore(NewIp, NewPassword, NewUrl)
    if res:
        logger.info(str(no) +' : '+ NewIp + " restore success")
    else:
        logger.warning(str(no) +' : '+ NewIp + " restore failed")

if __name__ == '__main__':
    NewIps = [key for key in NewIps if key != '']
    pool = Pool(len(NewIps))
    for i in range(len(NewIps)):
        pool.apply_async(main, (i,))
    pool.close()
    pool.join()

