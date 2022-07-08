import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy

i=0
more=8
max=255
max_test=3
begin=0
#data格式为第一行ip，pasword，三个值
data=xlrd.open_workbook("./data.xls",formatting_info=True)
data1=xlrd.open_workbook("./allnewdata.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)
Mnemonic_List=table.col_values(2)
PeerID_List=table.col_values(3)
PrivKey_List=table.col_values(4)
excel=copy(data1)
#行数
row=table.nrows

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'failed')
tables.write(0, 3, 'geshu')
tables.write(0, 4, 'Mnemonic')
tables.write(0, 5, 'PeerID')
tables.write(0, 6, 'PrivKey')


while row > i:
    count=0
    success=False
    while count < max_test and not success:
        while ip_List[i+1]=='' or password_List[i+1]=='':
            print('完成')
            sys.exit(0)
        try:
            username='root'
            port= 22
            ip=ip_List[i+1]
            password=password_List[i+1]
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
                tables.write(begin+1,2,'loginfailed')
                mingzi='allnewdata.xls'
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
        command = "ls -a | grep -E '.btfs[1-9]+' | wc -l"
        stdin,stdout,stderr=client.exec_command(command)
        maxnumber = stdout.readlines()[0].strip()
        maxnumber = int(maxnumber)
        if maxnumber>=more:
            print('已存在'+str(maxnumber)+'个应用')
            break
        while more > maxnumber:
            command='ls'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.readlines()
            maxnumber=0
            command = "ls -a | grep -E '.btfs[1-9]+' | wc -l"
            stdin,stdout,stderr=client.exec_command(command)
            maxnumber = stdout.readlines()[0].strip()
            maxnumber = int(maxnumber)
            print(maxnumber)
            command='cp -r btfs btfs'+str(maxnumber+1)
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
                tables.write(begin+1, 2, 'copy失败')
            else:
                print('copy成功')

            suc=False
            test_test=3
            while suc is False and (test_test != 0):
                chan = client.invoke_shell()
                chan.send('export BTFS_PATH=/root/.btfs'+str(maxnumber+1)+'\n')
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
                    tables.write(begin+1, 2, 'init失败')
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
                    if date.find('config')!=-1:
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
            newport=int(float(duankou))      #5001
            newadd=newport-5001
            newport1=8080+newadd        #8080
            newport2=6101+newadd        #5101
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
                while  data.find("PeerID",0,len(data))!=-1 and find1==False:
                    zifu1=data.find("PeerID",0,len(data))
                    find1=True
                    wri1=data[zifu1+10:len(data)-3]
                    print(wri1)
            for data in results:
                while  data.find("PrivKey",0,len(data))!=-1 and find2==False:
                    zifu2=data.find("PrivKey",0,len(data))
                    find2=True
                    wri2=data[zifu2+11:len(data)-2]
                    print(wri2)
            for data in results:
                while  data.find("Mnemonic",0,len(data))!=-1 and find==False:
                    zifu=data.find("Mnemonic",0,len(data))
                    find=True
                    wri=data[zifu+12:len(data)-3]
                    print(wri)
            s1="sed -i 's/"+wri+"/"+Mnemonic_List[begin+1]+"/' .btfs"+str(maxnumber+1)+"/config"
            print(s1)
            command=(s1)
            stdin, stdout, stderr = client.exec_command(command)
            s2="sed -i 's/"+wri1+"/"+PeerID_List[begin+1]+"/' .btfs"+str(maxnumber+1)+"/config"
            print(s2)
            command=(s2)
            stdin, stdout, stderr = client.exec_command(command)
            s3="sed -i 's/"+wri2.replace('/','\/')+"/"+PrivKey_List[begin+1].replace('/','\/')+"/' .btfs"+str(maxnumber+1)+"/config"
            print(s3)
            command=(s3)
            stdin, stdout, stderr = client.exec_command(command)
            print(begin+1)
            tables.write(begin+1, 0, ip)
            tables.write(begin+1, 1, password)
            tables.write(begin+1, 3, maxnumber+1)
            tables.write(begin+1, 4, Mnemonic_List[begin+1])
            tables.write(begin+1, 5, PeerID_List[begin+1])
            tables.write(begin+1, 6, PrivKey_List[begin+1] )
            wri=''
            wri1=''
            wri2=''
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
            excel.save('allnewdata.xls')
            sleep(3)
            print("完成")
            maxnumber+=1
        client.close()
    else:
        print("连接失败")
        sys.exit(0)
    max=0
    i=i+1
    success=False
