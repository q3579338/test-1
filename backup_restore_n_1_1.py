import os
import paramiko
import xlrd
import xlwt
import logging
from multiprocessing import Pool

#删除旧机压缩文件
OldDelAfterRestore = True

logging.basicConfig(level=logging.INFO , format   = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
logger = logging.getLogger()

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

OldIps = table.col_values(0)
OldPasswords = table.col_values(1)

NewIps = table.col_values(2)
NewPasswords = table.col_values(3)

key = 1
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
    FileName = 'btt.tar' 
    if client:
        command = 'rm -rf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        #logger.info('kill screen')
        command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        TarFileName = '.btfs*'
        command = 'tar -cvf '+ FileName +' btfs '+ TarFileName
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
        command = "nohup /root/chfs --port 55555 > chf.log 2>&1 &"
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
    
def restore(OldIp , NewIp , NewPassword , index , over):
    global key
    OldIp = OldIp.strip()
    NewIp = NewIp.strip()
    NewPassword = NewPassword.strip()
    client = connect(NewIp , NewPassword)
    FileName = 'btt.tar'
    if client:
        if index == 0:
            command='ls -a /root'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.readlines()
            MaxNumber = 0
            for data in res:
                geshu=data.find('.btfs')
                shu=data.replace('.btfs','').replace('\n','')
                if geshu!=-1:
                    if shu=='':
                        shu=0
                    else:
                        shu=int(shu)
                    if shu > MaxNumber:
                        MaxNumber = shu
            key = MaxNumber+1

        command = 'rm -rf tmp'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'mkdir tmp'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'rm -rf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'apt install -y axel'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'axel -n 16 -o /root/tmp/'+FileName+' http://'+ OldIp +':55555/chfs/shared/'+ FileName +' -q'
        logger.info(command)
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'cd tmp && tar -xvf ' + FileName
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
    
        command='ls -a /root/tmp/'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        MaxNumber = 0
        for data in res:
            geshu=data.find('.btfs')
            shu=data.replace('.btfs','').replace('\n','')
            if geshu!=-1:
                if shu=='':
                    shu=0
                else:
                    shu=int(shu)
                if shu > MaxNumber:
                    MaxNumber = shu
        #print(MaxNumber)

        command = 'cd tmp && rm -rf .btfs && rm -rf btt.tar && rm -rf btt.tar.st'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        #修改索引
        tmp = 1
        for i in range(1 , MaxNumber+1):
            command = 'cd tmp && mv .btfs'+str(i)+' .btfs'+str(key)
            print(command)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            command = 'cd tmp && mv .btfs'+str(key)+' /root'
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            key+=1
        
        command = 'rm -rf tmp/*'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()

        if over:
            command = 'cd tmp && mv btfs /root'
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()
            command = 'rm -rf tmp'
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()

            command='ls -a'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.readlines()
            MaxNumber = 0
            for data in res:
                geshu=data.find('.btfs')
                shu=data.replace('.btfs','').replace('\n','')
                if geshu!=-1:
                    if shu=='':
                        shu=0
                    else:
                        shu=int(shu)
                    if shu > MaxNumber:
                        MaxNumber = shu
            #print(MaxNumber)
            op = ''
            for i in range(1 , MaxNumber+1):
                op += 'btfs'+str(i)+' '
            command = 'echo '+op+'|'+'xargs -n1 cp -r btfs'
            #logger.info(command)
            stdin, stdout, stderr = client.exec_command(command)
            res = stdout.readlines()

            #修改端口
            OldPort1 = 5001
            OldPort2 = 8080
            OldPort3 = 6101
            OldPort4 = 4001

            for i in range(1 , MaxNumber+1):
                print(f"进度 {i} / {MaxNumber}")
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

        ##################################################
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

    p = Pool(len(OldIps))
    res = []
    for i in range(len(OldIps)):
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
    
    for i in range(len(OldIps)):
        NewIp = NewIps[no]
        NewPassword = NewPasswords[no]
        OldIp = OldIps[i]
        if i == len(OldIps)-1:
            status , msg = restore(OldIp,NewIp,NewPassword,i , True)
        else:
            status , msg = restore(OldIp,NewIp,NewPassword,i , False)
        if status == False:
            tables.write(flag, 0, OldIp)
            tables.write(flag, 1, NewIp)
            tables.write(flag, 2, msg)
            flag += 1
        
    # if OldDelAfterRestore:
    #     if 'tar' in Compress:
    #         FileName = 'btt.tar'
    #     elif 'zip' in Compress:
    #         FileName = 'btt.zip'
    #     logger.info('del OldIp tar or zip file')
    #     delfile(OldIp , OldPassword , FileName)

if __name__ == '__main__':
    OldIps = [key for key in OldIps if key != '']
    OldPasswords = [key for key in OldPasswords if key != '']
    NewIps = [key for key in NewIps if key != '']
    NewPasswords = [key for key in NewPasswords if key != '']
    main(0)

