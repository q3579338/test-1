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
from multiprocessing import Pool

#原机子btfs数量
OldBtfsNumbers = 8
#一个新的上面几个旧的
OldNumbers = 8
#压缩方式 可选 tar , zip
Compress = 'tar'
#删除旧机压缩文件
OldDelAfterRestore = True

logging.basicConfig(level=logging.INFO , format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
logger = logging.getLogger()

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

def back(OldIp , OldPassword):
    OldIp = OldIp.strip()
    OldPassword = OldPassword.strip()
    client = connect(OldIp , OldPassword)
    if 'tar' in Compress:
        FileName = 'btt.tar'
    elif 'zip' in Compress:
        FileName = 'btt.zip'    
    if client:
        command = 'rm -rf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        #logger.info('kill screen')
        command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        TarFileName = '.btfs*'
        if 'tar' in Compress:
            command = 'tar -cvf '+ FileName +' btfs '+ TarFileName
            #logger.info(command)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
        elif 'zip' in Compress:
            command = 'zip -r '+ FileName +' btfs '+ TarFileName
            #logger.info(command)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
    else:
        failed = 'connect failed'
        return False , failed
    if res == []:
        failed = 'zip or tar failed'
        return False , failed
    
    command = 'netstat -tunlp | grep 55555'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.readlines()
    if 'chfs' not in ''.join(res):
        logger.info(OldIp+' start chfs')
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
    return True , 'success'
    
def restore(OldIp , NewIp , NewPassword , index):
    OldIp = OldIp.strip()
    NewIp = NewIp.strip()
    NewPassword = NewPassword.strip()
    client = connect(NewIp , NewPassword)
    if 'tar' in Compress:
        FileName = 'btt.tar'
    elif 'zip' in Compress:
        FileName = 'btt.zip'
    if client:
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
        
        if index%OldNumbers == 0:
            index = OldNumbers
        else:
            index = index%OldNumbers

        tmp = 1
        for i in range( (OldNumbers-index)*OldBtfsNumbers + 1 , (OldNumbers+1-index)*OldBtfsNumbers+1):
            command = 'mv .btfs'+str(tmp)+' .btfs'+str(i)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            tmp+=1

        op = ''
        for i in range((OldNumbers-index)*OldBtfsNumbers + 1 , (OldNumbers+1-index)*OldBtfsNumbers+1):
            op += 'btfs'+str(i)+' '
        command = 'echo '+op+'|'+'xargs -n1 cp -r btfs'
        logger.info(command)
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()

        OldPort1 = 5001
        OldPort2 = 8080
        OldPort3 = 6101
        OldPort4 = 4001

        for i in range( (OldNumbers-index)*OldBtfsNumbers + 1 , (OldNumbers+1-index)*OldBtfsNumbers+1):

            command0 = "export BTFS_PATH=/root/.btfs" + str(i)

            command1 = "export PATH=${PATH}:${HOME}/btfs" + str(i) + "/bin"

            command2 = "btfs config Addresses.API /ip4/127.0.0.1/tcp/" + str(int(OldPort1) + int(i))

            command3 = "btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/" + str(int(OldPort2) + int(i))

            command4 = "btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/" + str(int(OldPort3) + int(i))

            command5 = "btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(int(OldPort4) + int(i))+"\""+",\"/ip6/::/tcp/"+str(int(OldPort4) + int(i))+"\""+"]'"
            
            command = command0 + "&&" + command1 + "&&" + command2
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            command = command0 + "&&" + command1 + "&&" + command3
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            command = command0 + "&&" + command1 + "&&" + command4
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            command = command0 + "&&" + command1 + "&&" + command5
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
        
        command = 'rm -rf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        # command = 'rm -rf ' + FileName
        # stdin, stdout, stderr = client.exec_command(command)
        # res = stdout.readlines()
        # command = 'rm -rf auto_btt_test.py'
        # stdin, stdout, stderr = client.exec_command(command)
        # res = stdout.readlines()
        # command = 'rm -rf screen_btt_test.py'
        # stdin, stdout, stderr = client.exec_command(command)
        # res = stdout.readlines()
        # command = 'curl -O https://raw.githubusercontent.com/0honus0/test/main/auto_btt_test.py'
        # stdin, stdout, stderr = client.exec_command(command)
        # res = stdout.readlines()
        # command = "screen -Smd run python3 auto_btt_test.py"
        # stdin, stdout, stderr = client.exec_command(command)
        # res = stdout.readlines()
        # logger.info('***************************************')
        # logger.info(NewIp + " Btfs Start BackGround Running.")
        # logger.info('***************************************')
        client.close()
        return True ,  'success'


def main(no):
    global flag

    p = Pool(OldNumbers)
    res = []
    for i in range(no*OldNumbers , (no+1)*OldNumbers ):
        OldIp = OldIps[i]
        OldPassword = OldPasswords[i]
        q = p.apply_async(back, (OldIp,OldPassword,))
        res.append(q)
    p.close()
    p.join()
    for data in res:
        k = data.get()
        status = k[0]
        msg = k[1]
        if status == False:
            tables.write(flag, 0, OldIp)
            tables.write(flag, 1, NewIp)
            tables.write(flag, 2, msg)
            flag+=1
    
    for i in range(no*OldNumbers + 1 , (no+1)*OldNumbers + 1):
        NewIp = NewIps[no]
        NewPassword = NewPasswords[no]
        OldIp = OldIps[i-1]
        status , msg = restore(OldIp,NewIp,NewPassword,i)
        if status == False:
            tables.write(flag, 0, OldIp)
            tables.write(flag, 1, NewIp)
            tables.write(flag, 2, msg)
            flag += 1
        
    if OldDelAfterRestore:
        if 'tar' in Compress:
            FileName = 'btt.tar'
        elif 'zip' in Compress:
            FileName = 'btt.zip'
        logger.info('del OldIp tar or zip file')
        delfile(OldIp , OldPassword , FileName)

if __name__ == '__main__':
    OldIps = [key for key in OldIps if key != '']
    OldPasswords = [key for key in OldPasswords if key != '']
    NewIps = [key for key in NewIps if key != '']
    NewPasswords = [key for key in NewPasswords if key != '']
    for i in range(len(NewIps)):
        main(i)

