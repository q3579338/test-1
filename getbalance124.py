import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
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
tables.write(0, 9, 'active_contract_num')
tables.write(0, 10, 'Online')
tables.write(0, 11, 'check')
tables.write(0, 12, 'uptime_score')
tables.write(0, 13, 'age_score')
tables.write(0, 14, 'version_score')
tables.write(0, 15, 'speed_score')
tables.write(0, 16, 'Uptime')
tables.write(0, 17, 'screen_count')

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
                tables.write(begin+1,11,'loginfailed')
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

        command='screen -ls'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        pat='(\d+) Sockets in'
        try:
            screen_count=re.search(pat,''.join(res)).group(1)
            print('screen_count: '+str(screen_count))
            tables.write(1, 17, screen_count)
        except:
            pass
        lis=1
        while lis < maxnumber+1:
            try:
                Score=''
                BttWalletBalance=''
                Storage_used=''
                Online=''
                Uptime_score=''
                Age_score=''
                Version_score=''
                Speed_score=''
                Uptime=''
                print(str(lis)+'/'+str(maxnumber))
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
                    chan.send('btfs storage contracts stat host\n')
                    sleep(5)
                    result=bytes.decode(chan.recv(4096))
                    pat='active_contract_num":(\d+),'
                    active_contract_num=re.search(pat,result).group(1)
                    tables.write(begin+1, 9, active_contract_num)
                    print('"active_contract_num":'+str(active_contract_num))
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
                        tables.write(begin+1,11,'getScorefailed')
                        mingzi=time+".xls"
                        two=two+1
                        excel.save(mingzi)
                        print('数据为空')
                        lis=lis+1
                        begin=begin+1
                        continue
                    print(Score[:])
                    print(Storage_used[:])
                    print(Online[:-1])
                    print(Uptime_score[:])
                    print(Age_score[:])
                    print(Version_score[:])
                    print(Speed_score[:])
                    print(Uptime[:])
                    tables.write(begin+1,6,Score[8:])
                    tables.write(begin+1,8,int(Storage_used[15:])/1024/1024)
                    tables.write(begin+1,10,Online[9:-1])
                    tables.write(begin+1,12, Uptime_score[15:])
                    tables.write(begin+1,13, Age_score[12:])
                    tables.write(begin+1,14, Version_score[16:])
                    tables.write(begin+1,15, Speed_score[14:])
                    tables.write(begin+1,16, Uptime[9:])
                    updata_time=Uptime[9:]
                    chan.send('btfs vault balance\n')
                    sleep(5)
                    result=bytes.decode(chan.recv(2048))
                    data=result
                    if 'available balance' in data:
                        pat='the vault available balance: (0|([1-9]\d*))(\.\d+)?'
                        BttWalletBalance=re.search(pat,data)
                        if BttWalletBalance!=None:
                            BttWalletBalance=BttWalletBalance.group(0)
                        print(str(BttWalletBalance))
                    else:
                        tables.write(begin+1,11,'getBttWalletfailed')
                        print('数据为空')
                        two=two+1
                        mingzi=time+'.xls'
                        excel.save(mingzi)
                        lis=lis+1
                        begin=begin+1
                        continue
                    BttWalletBalance = BttWalletBalance.replace('the vault available balance: ', '')
                    if len(BttWalletBalance)>21:
                        BttWalletBalance=BttWalletBalance[:-21]
                    tables.write(begin+1,7,BttWalletBalance)
                # 8 19 25
                print("完成")
                mingzi=time+".xls"
                print(mingzi)
                excel.save(mingzi)
                begin=begin+1
                lis=lis+1
            except:
                two=two+1
                tables.write(begin+1,11,'runInterrupt')
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
