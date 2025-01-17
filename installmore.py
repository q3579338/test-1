import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy

i=0
more=3
max=255
max_test=3
begin=0

data=xlrd.open_workbook("D:/Study/python/data.xls",formatting_info=True)
data1=xlrd.open_workbook("D:/Study/python/alldata.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)
excel=copy(data1)
#行数
row=table.nrows

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'failed')
tables.write(0, 3, 'duokai')
tables.write(0, 4, 'Mnemonic')
tables.write(0, 5, 'PeerID')
tables.write(0, 6, 'PrivKey')

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
                tables.write(begin+1,0,ip_List[i])
                tables.write(begin+1,1,password)
                tables.write(begin+1,2,'loginfailed')
                mingzi='alldata.xls'
                print(mingzi)
                excel.save(mingzi)
                count=0
                i=i+1
                print('连接失败，开始下一个')
            else:
                print('登陆失败，尝试重新登陆')
                count =count+1
    if success:
        print("连接成功")
        command='ls /root/data'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        maxnumber=0
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
        if maxnumber-1>=more:
            print('已存在'+str(maxnumber)+'个应用')
            break
        while more-maxnumber>1:
            command='ls'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.readlines()
            maxnumber=0
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
            command='cp -r btfs btfs'+str(maxnumber+1)
            print(command)
            stdin, stdout, stderr = client.exec_command(command)
            command='ls -a'
            stdin, stdout, stderr = client.exec_command(command)
            res=stdout.readlines()
            find=False
            pat='btfs'+str(maxnumber+1)
            print(pat)
            for data in res:
                if data.find(pat)!=-1 and find is False:
                    find=True
            if find is False:
                print('copy失败!!!')
                tables.write(i+1, 2, 'copy失败')
            else:
                print('copy成功')

            suc=False
            test_test=3
            while suc is False and (test_test != 0):
                chan = client.invoke_shell()
                chan.send('cd /root/data\n')
                sleep(1)
                chan.send('export BTFS_PATH=/root/data/.btfs'+str(maxnumber+1)+'\n')
                sleep(2)
                chan.send('export PATH=${PATH}:${HOME}/btfs'+str(maxnumber+1)+'/bin\n')
                sleep(2)
                chan.send('btfs init\n')
                sleep(2)

                command='ls -a'
                stdin, stdout, stderr = client.exec_command(command)
                results = stdout.readlines()
                #print(results)

                for data in results:
                    pat='.btfs'+str(maxnumber+1)
                    #print(pat)
                    if data.find(pat)!=-1:
                        suc=True
                if suc:
                    print("btfs"+str(maxnumber+1)+" init成功")
                elif test_test!=0:
                    print("初始化失败,重试")
                    test_test=test_test-1
                elif test_test==0:
                    tables.write(i+1, 2, 'init失败')
                    print('失败')



            chenggong=False
            while chenggong is False:
                chan.send('btfs config profile apply storage-host\n')
                sleep(5)
                print("执行btfs config profile apply storage-host中...")
                command=('ls .btfs'+str(maxnumber+1)+'/ -a')
                #print(command)
                stdin, stdout, stderr = client.exec_command(command)
                results = stdout.readlines()
                #print(results)
                flag=False
                for date in results:
                    if date.find('config-pre-storage-host')!=-1:
                        print('执行apply成功')
                        chenggong=True

            command='apt-get -y install screen'
            stdin, stdout, stderr = client.exec_command(command)
            sleep(2)

            if maxnumber==0:
                command=command='cat .btfs/config'
            else:
                command='cat .btfs'+str(maxnumber)+'/config'
            print(command)
            stdin, stdout, stderr = client.exec_command(command)
            res=stdout.readlines()
            duankou=''
            for data in res:
                pat='\"API\": \"/ip4/127.0.0.1/tcp/[0-9]*'
                if re.search(pat,data)!=None:
                    duankou=re.search(pat,data).group()
                    duankou=duankou[27:len(data)-1]
            print(duankou)
            newport=int(float(duankou))+1      #5001
            newadd=newport-5001
            newport1=8080+newadd        #8080
            newport2=5101+newadd        #5101
            newport3=4001+newadd        #4001
            print(newport)
            print(newport1)
            print(newport2)
            print(newport3)
            command='btfs config Addresses.API /ip4/127.0.0.1/tcp/'+str(newport)+'\n'
            print(command)
            chan.send(command)
            sleep(1)
            command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/'+str(newport1)+'\n'
            print(command)
            chan.send(command)
            sleep(1)
            command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/'+str(newport2)+'\n'
            print(command)
            chan.send(command)
            sleep(1)
            command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(newport3)+"\""+",\"/ip6/::/tcp/"+str(newport3)+"\""+"]'"+"\n"
            print(command)
            chan.send(command)
            sleep(1)

            command=('cat .btfs'+str(maxnumber+1)+'/config')
            stdin, stdout, stderr = client.exec_command(command)
            results = stdout.readlines()
            find=False
            find1=False
            find2=False
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
            tables.write(begin+1, 3, maxnumber+1)
            tables.write(begin+1, 4, Mnemonic)
            tables.write(begin+1, 5, PeerID)
            tables.write(begin+1, 6, PrivKey)
            begin=begin+1

            chan.send('screen -S btfs'+str(maxnumber+1)+'\n')
            sleep(3)
            chan.send('export BTFS_PATH=/root/.btfs'+str(maxnumber+1)+'\n')
            sleep(2)
            chan.send('export PATH=${PATH}:${HOME}/btfs'+str(maxnumber+1)+'/bin\n')
            sleep(2)
            chan.send('btfs daemon\n')
            sleep(5)

            # print("开始后台执行。。。")
            excel.save('alldata.xls')
            sleep(3)
            print("完成")
            #more=more-1
        client.close()
    else:
        print("连接失败")
        sys.exit(0)
    max=0
    i=i+1
    success=False
