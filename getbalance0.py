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
two=0

time=time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
print(time)
data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('BttWallet')
tables1 = excel.add_sheet('failed')

tables=excel.get_sheet('BttWallet')
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'duokai')
tables.write(0, 3, 'Mnemonic')
tables.write(0, 4, 'PeerID')
tables.write(0, 5, 'PrivKey')
tables.write(0, 6, 'Score')
tables.write(0, 7, 'BttWalletBalance')
tables.write(0, 8, 'Storage_used')
tables.write(0, 9, 'Online')
tables.write(0, 10, 'check')
tables.write(0, 11, 'uptime_score')
tables.write(0, 12, 'age_score')
tables.write(0, 13, 'version_score')
tables.write(0, 14, 'speed_score')
tables.write(0, 15, 'Uptime')
tables.write(0, 16, 'APIport')
tables.write(0, 17, 'Gatewayport')
tables.write(0, 18, 'RemoteAPIport')
tables.write(0, 19, 'Swarmport')

tables1.write(0, 0, 'ip')
tables1.write(0, 1, 'password')
tables1.write(0, 2, 'lis')
tables1.write(0, 3, 'uptime')
tables1.write(0, 4, 'check')
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
                tables.write(begin+1,10,'loginfailed')
                mingzi=time+".xls"
                print(mingzi)
                excel.save(mingzi)
                #i=i+1
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
        lis=0
        oldport=4001
        while lis < maxnumber+1:
            try:
                print(oldport)
                Score=''
                BttWalletBalance=''
                Storage_disk_available=''
                Online=''
                Uptime_score=''
                Age_score=''
                Version_score=''
                Speed_score=''
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
                duankou1=''
                duankou2=''
                duankou3=''
                for data in res:
                    pat='\"API\": \"/ip4/127.0.0.1/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou0=re.search(pat,data).group()
                        duankou0=duankou0[27:len(data)-1]
                for data in res:
                    pat='\"Gateway\": \"/ip4/127.0.0.1/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou1=re.search(pat,data).group()
                        duankou1=duankou1[31:len(data)-1]
                for data in res:
                    pat='\"RemoteAPI\": \"/ip4/127.0.0.1/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou2=re.search(pat,data).group()
                        duankou2=duankou2[33:len(data)-1]
                for data in res:
                    pat='\"/ip4/0.0.0.0/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou3=re.search(pat,data).group()
                        duankou3=duankou3[18:len(data)-1]

                print(duankou0)
                print(duankou1)
                print(duankou2)
                print(duankou3)
                print('\n')

                tables.write(begin+1, 16, str(duankou0))
                tables.write(begin+1, 17, str(duankou1))
                tables.write(begin+1, 18, str(duankou2))
                tables.write(begin+1, 19, str(duankou3))
                newport=int(float(duankou0))
                newadd=newport-5001
                duankou=4001+newadd

                newadd=oldport-4001
                newport0=5001+newadd
                newport1=8080+newadd        #8080
                newport2=5101+newadd        #5101
                newport3=4001+newadd        #4001

                print(newport0)
                print(newport1)
                print(newport2)
                print(newport3)
                if int(duankou0)!=int(newport0) or int(duankou1)!=int(newport1) or int(duankou2)!=int(newport2) or int(duankou3)!=int(newport3):
                    suc=False
                    test_test=3
                    chan = client.invoke_shell()
                    while suc is False and (test_test > 0):
                        if lis==0:
                            chan.send('export BTFS_PATH=/root/.btfs\n')
                        else:
                            chan.send('export BTFS_PATH=/root/.btfs'+str(lis)+'\n')
                        sleep(2)
                        if lis==0:
                            chan.send('export PATH=${PATH}:${HOME}/btfs/bin\n')
                        else:
                            chan.send('export PATH=${PATH}:${HOME}/btfs'+str(lis)+'/bin\n')
                        sleep(2)
                        chan.send('btfs init\n')
                        sleep(2)

                        command='ls -a'
                        stdin, stdout, stderr = client.exec_command(command)
                        results = stdout.readlines()
                        #print(results)

                        for data in results:
                            if lis==0:
                                pat='.btfs'
                            else:
                                pat='.btfs'+str(lis)
                            #print(pat)
                            if data.find(pat)!=-1:
                                suc=True
                        if suc:
                            print("btfs"+str(lis)+" init成功")
                        elif test_test!=0:
                            print("初始化失败,重试")
                            test_test=test_test-1
                        elif test_test==0:
                            tables.write(i+1, 10, 'init失败')
                            print('失败')
                            lis=lis+1
                            begin=begin+1
                            continue

                    chenggong=False
                    apply_test=3
                    while chenggong is False and apply_test>0:
                        chan.send('btfs config profile apply storage-host\n')
                        sleep(5)
                        print("执行btfs config profile apply storage-host中...")
                        if lis==0:
                            command=('ls .btfs/ -a')
                        else:
                            command=('ls .btfs'+str(lis)+'/ -a')
                        #print(command)
                        stdin, stdout, stderr = client.exec_command(command)
                        results = stdout.readlines()
                        #print(results)
                        flag=False
                        for date in results:
                            if date.find('config-pre-storage-host')!=-1:
                                print('执行apply成功')
                                chenggong=True
                            elif apply_test==0:
                                tables.write(i+1, 10, 'apply失败')
                                print('失败')
                                lis=lis+1
                                begin=begin+1
                                continue
                        apply_test=apply_test-1

                        #修改端口
                        if lis==0:
                            command=command='cat .btfs/config'
                        else:
                            command='cat .btfs'+str(lis)+'/config'
                        print(command)
                        stdin, stdout, stderr = client.exec_command(command)
                        res=stdout.readlines()

                        command='btfs config Addresses.API /ip4/127.0.0.1/tcp/'+str(newport0)+'\n'
                        print(command)
                        chan.send(command)
                        sleep(2)
                        command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/'+str(newport1)+'\n'
                        print(command)
                        chan.send(command)
                        sleep(2)
                        command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/'+str(newport2)+'\n'
                        print(command)
                        chan.send(command)
                        sleep(2)
                        command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(newport3)+"\""+",\"/ip6/::/tcp/"+str(newport3)+"\""+"]'"+"\n"
                        print(command)
                        chan.send(command)
                        sleep(2)

                        chan = client.invoke_shell()
                        if lis==0:
                            com='screen -S btfs\n'
                        else:
                            com='screen -S btfs'+str(lis)+'\n'
                        print(com)
                        chan.send(com)
                        sleep(2)
                        if lis==0:
                            com='export BTFS_PATH=/root/.btfs\n'
                        else:
                            com='export BTFS_PATH=/root/.btfs'+str(lis)+'\n'
                        print(com)
                        chan.send(com)
                        sleep(2)
                        if lis==0:
                            com='export PATH=${PATH}:${HOME}/btfs/bin\n'
                        else:
                            com='export PATH=${PATH}:${HOME}/btfs'+str(lis)+'/bin\n'
                        print(com)
                        chan.send(com)
                        sleep(2)
                        com='btfs daemon\n'
                        print(com)
                        chan.send(com)
                        sleep(4)
                command='apt -y install net-tools'
                stdin , stdout, stderr=client.exec_command(command)
                sleep(1)
                command='netstat -ntulp |grep '+str(oldport)
                oldport=oldport+1
                print(command)
                stdin , stdout, stderr=client.exec_command(command)
                result=stdout.readlines()
                #print(result)
                flag=False
                if result:
                    for data in result:
                        if data.find('btfs')!=-1:
                            flag=True
                else:
                    tables.write(begin+1,10,'runfailed')
                    chan = client.invoke_shell()
                    if lis==0:
                        com='screen -S btfs\n'
                    else:
                        com='screen -S btfs'+str(lis)+'\n'
                    print(com)
                    chan.send(com)
                    sleep(2)
                    if lis==0:
                        com='export BTFS_PATH=/root/.btfs\n'
                    else:
                        com='export BTFS_PATH=/root/.btfs'+str(lis)+'\n'
                    print(com)
                    chan.send(com)
                    sleep(2)
                    if lis==0:
                        com='export PATH=${PATH}:${HOME}/btfs/bin\n'
                    else:
                        com='export PATH=${PATH}:${HOME}/btfs'+str(lis)+'/bin\n'
                    print(com)
                    chan.send(com)
                    sleep(2)
                    com='btfs daemon\n'
                    print(com)
                    chan.send(com)
                    sleep(4)
                    flag=True

                if flag:
                    if lis==0:
                        com='cat .btfs/config'
                    else:
                        com='cat .btfs'+str(lis)+'/config'
                    print("获取值"+com)
                    command=(com)
                    stdin, stdout, stderr = client.exec_command(command)
                    results = stdout.readlines()
                    #print(results)

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
                    sleep(2)
                    if lis==0:
                        chan.send('export PATH=${PATH}:${HOME}/btfs/bin\n')
                    else:
                        chan.send('export PATH=${PATH}:${HOME}/btfs'+str(lis)+'/bin\n')
                    sleep(2)
                    chan.send('btfs storage stats info\n')
                    sleep(5)
                    result=bytes.decode(chan.recv(2048))
                    #print(result)
                    data=result
                    panduan=data.find('key')
                    #print(panduan)
                    if panduan==-1:
                        pat='"score":[0-9]+([.]{1}[0-9]+){0,1}'
                        Score=re.search(pat,data)
                        if Score!=None:
                            Score=Score.group(0)
                        pat1='"storage_used":[0-9]+([.]{1}[0-9]+){0,1}'
                        Storage_used=re.search(pat1,data)
                        if Storage_used!=None:
                            Storage_used=Storage_used.group(0)
                        pat2='"online":(\w+),'
                        Online=re.search(pat2,data)
                        if Online!=None:
                            Online=Online.group(0)
                        pat3='"uptime_score":(\w+)'
                        Uptime_score=re.search(pat3,data)
                        if Uptime_score!=None:
                            Uptime_score=re.search(pat3,data).group(0)
                        pat4='"age_score":(\w+)'
                        Age_score=re.search(pat4,data)
                        if Age_score!=None:
                            Age_score=re.search(pat4,data).group(0)
                        pat5='"version_score":(\w+)'
                        Version_score=re.search(pat5,data)
                        if Version_score!=None:
                            Version_score=re.search(pat5,data).group(0)
                        pat6='"speed_score":(\w+)'
                        Speed_score=re.search(pat6,data)
                        if Speed_score!=None:
                            Speed_score=re.search(pat6,data).group(0)
                        pat7='"uptime":[0-9]+([.]{1}[0-9]+){0,1}'
                        Uptime=re.search(pat7,data)
                        if Uptime!=None:
                            Uptime=re.search(pat7,data).group(0)
                    else:
                        tables.write(begin+1,10,'getScorefailed')
                        tables1.write(two+1,0,ip)
                        tables1.write(two+1,1,password)
                        tables1.write(two+1,2,lis)
                        tables1.write(two+1,4,'getScorefailed')
                        two=two+1
                        mingzi=time+".xls"
                        excel.save(mingzi)
                        print('数据为空')
                        lis=lis+1
                        begin=begin+1
                        continue
                    chan.send('btfs wallet balance\n')
                    sleep(5)
                    result=bytes.decode(chan.recv(2048))
                    data=result
                    if 'BttWalletBalance' in data:
                        pat='"BttWalletBalance":[0-9]+([.]{1}[0-9]+){0,1}'
                        BttWalletBalance=re.search(pat,data)
                        if BttWalletBalance!=None:
                            BttWalletBalance=BttWalletBalance.group(0)
                    else:
                        tables.write(begin+1,10,'getBttWalletfailed')
                        print('数据为空')
                        tables1.write(two+1,0,ip)
                        tables1.write(two+1,1,password)
                        tables1.write(two+1,2,lis)
                        tables1.write(two+1,4,'getBttWalletfailed')
                        two=two+1
                        mingzi=time+'.xls'
                        excel.save(mingzi)
                        lis=lis+1
                        begin=begin+1
                        continue
                    print('start')
                    print(Score[:])
                    print(BttWalletBalance[:])
                    print(Storage_used[:])
                    print(Online[:-1])
                    print(Uptime_score[:])
                    print(Age_score[:])
                    print(Version_score[:])
                    print(Speed_score[:])
                    print(Uptime[:])
                    tables.write(begin+1,6,Score[8:])
                    tables.write(begin+1,7,BttWalletBalance[19:])
                    tables.write(begin+1,8,int(Storage_used[15:])/1024/1024)
                    tables.write(begin+1,9,Online[9:-1])
                    tables.write(begin+1,11, Uptime_score[15:])
                    tables.write(begin+1,12, Age_score[12:])
                    tables.write(begin+1,13, Version_score[16:])
                    tables.write(begin+1,14, Speed_score[14:])
                    tables.write(begin+1,15, Uptime[9:])
                    updata_time=Uptime[9:]
                    if float(updata_time)<0.96:
                        tables1.write(two+1,0,ip)
                        tables1.write(two+1,1,password)
                        tables1.write(two+1,2,lis)
                        tables1.write(two+1,3,updata_time)
                        two=two+1
                # 8 19 25
                if flag is False:
                    tables.write(begin+1, 0,ip)
                    tables.write(begin+1, 1,password)
                    tables.write(begin+1, 2, lis)
                    tables.write(begin+1, 9,'runfailed')
                    tables1.write(two+1,0,ip)
                    tables1.write(two+1,1,password)
                    tables1.write(two+1,2,lis)
                    tables1.write(two+1,4,'runfailed')
                    two=two+1
                print("完成")
                mingzi=time+".xls"
                print(mingzi)
                excel.save(mingzi)
                begin=begin+1
                lis=lis+1
            except:
                tables1.write(two+1,0,ip)
                tables1.write(two+1,1,password)
                tables1.write(two+1,2,lis)
                tables1.write(two+1,4,'runInterrupt')
                two=two+1
                tables.write(begin+1,10,'runInterrupt')
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
