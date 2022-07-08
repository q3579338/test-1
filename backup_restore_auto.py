'''
Author: honus
Date: 2022-03-09 21:04:21
LastEditTime: 2022-03-24 07:56:34
LastEditors: honus
Description:  64 -> 8 , 128 -> 16 , n -> n
FilePath: /test/backup_restore_auto.py
'''
import os
import paramiko
import xlrd
import xlwt
import logging

#原机子btfs数量
OldNumbers = 128
#新机子btfs数量
NewNumbers = 1
#压缩方式 可选 tar , zip
Compress = 'tar'
#删除旧机压缩文件
OldDelAfterRestore = True
#删除新机下载文件
NewDelAfterRestore = True

logging.basicConfig(level=logging.INFO , format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
logger = logging.getLogger('backup_restore')

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

OldIps = table.col_values(0)[1:]
OldPasswords = table.col_values(1)[1:]

NewIps = table.col_values(2)[1:]
NewPasswords = table.col_values(3)[1:]

flag = 1
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'OldIp')
tables.write(0, 1, 'NewIp')
tables.write(0, 2, 'Status')

def connect(ip,password):
    MaxTestNum = 3
    while True:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            logger.info(ip+" connect success")
            return client
        except:
            if MaxTestNum > 0:
                MaxTestNum -= 1
            else:
                return False

def delfile(Ip , PassWord , Name):
    client = connect(Ip , PassWord)
    if client:
        command = 'rm -rf ' + Name
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        client.close()
        return True
    else:
        return False

def back(OldIp , OldPassword , NewNumbers , index):
    OldIp = OldIp.strip()
    OldPassword = OldPassword.strip()
    client = connect(OldIp , OldPassword)
    if 'tar' in Compress:
        FileName = 'btt'+ str(index+1) +'.tar'
    elif 'zip' in Compress:
        FileName = 'btt'+ str(index+1) +'.zip'    
    if client:
        command = 'rm -rf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        logger.info('kill screen')
        command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        TarFileName = ''
        for k in range(index * NewNumbers + 1,(index+1) * NewNumbers + 1):
            TarFileName += '.btfs'+ str(k) +' '
        if 'tar' in Compress:
            command = 'tar -cvf '+ FileName +' btfs '+ TarFileName
            logger.info(command)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
        elif 'zip' in Compress:
            command = 'zip -r '+ FileName +' btfs '+ TarFileName
            logger.info(command)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
    else:
        failed = 'connect failed'
        return False , failed
    if res == []:
        failed = 'zip or tar failed'
        return False , failed
    
    command = 'md5sum ' + FileName
    stdin, stdout, stderr = client.exec_command(command)
    md5 = stdout.readlines()

    command = 'netstat -tunlp | grep 55555'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.readlines()
    if 'chfs' not in ''.join(res):
        logger.info('start chfs')
        command = 'wget https://github.com/0honus0/test/raw/main/chfs && chmod +x chfs'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = "nohup /root/chfs --port 55555 > chfs.log 2>&1 &"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'netstat -tunlp | grep 55555'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        if 'chfs' not in ''.join(res):
            failed = 'start chfs failed'
            return False , failed
    client.close()
    return True , md5
    
def restore(OldIp , NewIp , NewPassword , md5 , index):
    OldIp = OldIp.strip()
    NewIp = NewIp.strip()
    NewPassword = NewPassword.strip()
    client = connect(NewIp , NewPassword)
    if 'tar' in Compress:
        FileName = 'btt'+ str(index+1) +'.tar'
    elif 'zip' in Compress:
        FileName = 'btt'+ str(index+1) +'.zip'
    if client:
        command = 'rm -rf btfs'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'rm -rf .btfs'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'rm -rf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'apt install -y axel'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'axel -n 16 http://'+ OldIp +':55555/chfs/shared/'+ FileName +' -q'
        #command = 'wget http://'+str(OldIp)+':55555/' + FileName
        logger.info(command)
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'md5sum ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        md5_new = stdout.readlines()
        if md5_new != md5:
            failed = 'md5 not equal'
            return False , failed
        if 'tar' in Compress:
            command = 'tar -xvf ' + FileName
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
        elif 'zip' in Compress:
            command = 'unzip -o' + FileName
            try:
                stdin, stdout, stderr = client.exec_command(command , timeout=1200)
                res = stdout.readlines()
            except:
                failed = 'unzip timeout'
                return False , failed
        
        if NewNumbers == 1:
            command = 'mv .btfs'+ str(index + 1) +' .btfs'
            logger.info(command)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
        else:
            for i in range( index*NewNumbers + 1 , (index+1)*NewNumbers + 1):
                command = 'mv .btfs'+str(i)+' .btfs'+str(i-index*NewNumbers)
                stdin, stdout, stderr = client.exec_command(command)
                res = stdout.readlines()

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
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()

        if NewDelAfterRestore:
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
        logger.info(NewIp + " Btfs Start BackGround Running.")
        logger.info('***************************************')
        client.close()
        return True ,  'success'


def main(no):
    #OldNumbers 旧机子btfs数量
    #NewNumbers 新机子btfs数量
    #Block  n 台机子
    global flag
    Block = int(OldNumbers/NewNumbers)
    OldIp = OldIps[no]
    OldPassword = OldPasswords[no]

    for i in range(0,Block):
        try:
            NewIp = NewIps[no*Block+i]
            if NewIp == 'A':
                continue
            NewPassword = NewPasswords[no*Block+i]
            tables.write(flag, 0, OldIp)
            tables.write(flag, 1, NewIp)
        except:
            tables.write(flag, 2, 'NewIp or NewPassword not found')
            excel.save('backup_restore.xls')
            os._exit(0)

        Status , msg =  back(OldIp , OldPassword , NewNumbers , i)
        if not Status:
            tables.write(flag, 2, msg)
            excel.save('backup_restore.xls')
            flag += 1
            continue

        Status , msg =  restore(OldIp, NewIp, NewPassword, msg , i)
        if not Status:
            tables.write(flag, 2, msg)
            tables.save('backup_restore.xls')
            flag += 1
            continue
        
        if OldDelAfterRestore:
            if 'tar' in Compress:
                FileName = 'btt'+ str(i+1) +'.tar'
            elif 'zip' in Compress:
                FileName = 'btt'+ str(i+1) +'.zip'
            logger.info('del OldIp tar or zip file')
            delfile(OldIp , OldPassword , FileName)

        tables.write(flag, 2, 'success')
        flag += 1
        excel.save('backup_restore.xls')

if __name__ == '__main__':
    OldIps = [key for key in OldIps if key != '']
    for i in range(0,len(OldIps)):
        main(i)


