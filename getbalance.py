import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy
import time

i=0
max_test=3
maxnumber=0
begin=0

time=time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
print(time)
data=xlrd.open_workbook("./all.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('BttWallet')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'duokai')
tables.write(0, 3, 'Mnemonic')
tables.write(0, 4, 'PeerID')
tables.write(0, 5, 'PrivKey')
tables.write(0, 6, 'Score')
tables.write(0, 7, 'Storage_used')
tables.write(0, 8, 'Uptime')
tables.write(0, 9, 'running status')
tables.write(0, 10, 'used')
tables.write(0, 11, 'screen')


while row > i:
    count=0
    success=False


    while count < max_test and not success:
        try:
            username='root'
            port= 22
            ip=ip_List[i]
            password=password_List[i]
            print(ip)
            print(password)
            print('当前在第'+str(i+1)+'个')
            print('尝试第'+str(count+1)+'次登陆')
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port, username=username, password=password,timeout=30)
            success = True
        except:
            if count == max_test-1:
                tables.write(begin+1,0,ip)
                tables.write(begin+1,1,password)
                tables.write(begin+1,9,'loginfailed')
                mingzi=time+".xls"
                print(mingzi)
                excel.save(mingzi)
                i=i+1
                begin=begin+1
                count=0
                print('连接失败，开始下一个')
                break
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")

        #获取最大值
        command='ls'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
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
        print(maxnumber)
        try:
            command='free -m'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.readlines()
            res=res[1].split()
            tables.write(begin+1,10,str(res[2])+'/'+str(res[1]))
        except:
            pass
        try:
            command='screen -ls'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.readlines()
            countbtfs=0
            for name in res:
                if 'btfs' in name:
                    countbtfs+=1
            tables.write(begin+1,11,countbtfs)
        except:
            pass
        lis=1
        while lis < maxnumber+1:
            try:
                Score=''
                Storage_disk_available=''
                Uptime=''
                print(str(lis)+'/'+str(maxnumber))
                #检测port
                if lis==0:
                    command='cat .btfs/config'
                else:
                    command='cat .btfs'+str(lis)+'/config'
                print("获取端口"+command)
                stdin, stdout, stderr = client.exec_command(command)
                res=stdout.readlines()
                duankou0=''
                for data in res:
                    pat='\"/ip4/0.0.0.0/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou0=re.search(pat,data).group()
                        duankou0=duankou0[18:len(data)-1]

                command='apt -y install net-tools'
                stdin , stdout, stderr=client.exec_command(command)
                sleep(1)
                command='netstat -ntulp |grep '+str(duankou0)
                print(command)
                stdin , stdout, stderr=client.exec_command(command)
                result=stdout.readlines()
                flag=False
                if result:
                    for data in result:
                        if data.find('btfs')!=-1:
                            flag=True

                if flag:
                    print('正在运行。。。')
                    if lis==0:
                        com='cat .btfs/config'
                    else:
                        com='cat .btfs'+str(lis)+'/config'
                    print("获取值"+com)
                    command=(com)
                    stdin, stdout, stderr = client.exec_command(command)
                    results = stdout.readlines()

                    for data in results:
                        pat="\"Mnemonic\": (?:'|\").*(?:'|\")"
                        if re.search(pat , data)!=None:
                            Mnemonic = re.search(pat , data).group()
                            Mnemonic = Mnemonic[13:len(Mnemonic)-1]
                            print(Mnemonic)
                    for data in results:
                        pat="\"PeerID\": (?:'|\").*(?:'|\")"
                        if re.search(pat , data)!=None:
                            PeerID=re.search(pat , data).group()
                            PeerID = PeerID[11:len(PeerID)-1]
                            print(PeerID)
                    for data in results:
                        pat="\"PrivKey\": (?:'|\").*(?:'|\")"
                        if re.search(pat , data)!=None:
                            PrivKey=re.search(pat , data).group()
                            PrivKey =PrivKey[12:len(PrivKey)-1]
                            print(PrivKey)
                    tables.write(begin+1, 0, ip)
                    tables.write(begin+1, 1, password)
                    tables.write(begin+1, 2, lis)
                    tables.write(begin+1, 3, Mnemonic)
                    tables.write(begin+1, 4, PeerID)
                    tables.write(begin+1, 5, PrivKey)
                    Mnemonic=''
                    PeerID=''
                    PrivKey=''

                    chan = client.invoke_shell()
                    if lis==0:
                        chan.send('export BTFS_PATH=/root/.btfs\n')
                    else:
                        chan.send('export BTFS_PATH=/root/.btfs'+str(lis)+'\n')
                    sleep(1)
                    if lis==0:
                        chan.send('export PATH=${PATH}:${HOME}/btfs/bin\n')
                    else:
                        chan.send('export PATH=${PATH}:${HOME}/btfs'+str(lis)+'/bin\n')
                    sleep(1)
                    chan.send('btfs storage stats info\n')
                    sleep(5)
                    result=bytes.decode(chan.recv(2048))
                    data=result
                    panduan=data.find('key')
                    if panduan==-1:
                        pat='"score":[0-9]+([.]{1}[0-9]+){0,1}'
                        Score=re.search(pat,data)
                        if Score!=None:
                            Score=Score.group(0)
                        pat1='"storage_used":[0-9]+([.]{1}[0-9]+){0,1}'
                        Storage_disk_available=re.search(pat1,data)
                        if Storage_disk_available!=None:
                            Storage_disk_available=Storage_disk_available.group(0)

                        pat7='"uptime":[0-9]+([.]{1}[0-9]+){0,1}'
                        Uptime=re.search(pat7,data)
                        if Uptime!=None:
                            Uptime=re.search(pat7,data).group(0)
                    else:
                        tables.write(begin+1,9,'getScorefailed')
                        mingzi=time+".xls"
                        excel.save(mingzi)
                        print('数据为空')
                        lis=lis+1
                        begin=begin+1
                        continue
                    print('start')
                    print(Score[:])
                    print(Storage_disk_available[:])
                    print(Uptime[:])
                    tables.write(begin+1,6,Score[8:])
                    tables.write(begin+1,7,int(Storage_disk_available[15:])/1024/1024)
                    tables.write(begin+1,8, Uptime[9:])
                # 8 19 25
                if flag is False:
                    tables.write(begin+1, 0,ip)
                    tables.write(begin+1, 1,password)
                    tables.write(begin+1, 2, lis)
                    tables.write(begin+1, 9,'runfailed')
                    continue
                print("完成")
                tables.write(begin+1,9,'runsuc')
                mingzi=time+".xls"
                print(mingzi)
                excel.save(mingzi)
                begin=begin+1
                lis=lis+1
            except:
                tables.write(begin+1,9,'runInterrupt')
                begin=begin+1
                lis=lis+1
                mingzi=time+".xls"
                excel.save(mingzi)
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    if row+1!=maxnumber:
        i=i+1
