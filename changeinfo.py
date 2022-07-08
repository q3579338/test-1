import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy

i=0
max=255
max_test=3

data=xlrd.open_workbook("D:/change/alldata.xls",formatting_info=True)
data1=xlrd.open_workbook("D:/change/allnewdata.xls",formatting_info=True)
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
tables.write(0, 2, 'str')

while row > i+1:
    count=0
    success=False
    while count < max_test and not success:
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
            print('登陆失败，尝试重新登陆')
            sleep(1)
            count +=1
            if count == max_test:
                 break
    if success:
        print("连接成功")

        command='wget https://raw.githubusercontent.com/TRON-US/btfs-binary-releases/master/install.sh'
        print("执行wget中...")
        stdin, stdout, stderr = client.exec_command(command)

        max=3
        print("执行install.sh中...")
        succeeded=False
        while max>0 and not succeeded:
            command='bash install.sh -o linux -a amd64'
            stdin, stdout, stderr = client.exec_command(command)
            results = stdout.readlines()
            sleep(3)
            for data in results:
                #print(data)
                if data.find('succeeded')!=-1:
                    succeeded=True
            if succeeded and max>0:
                print('安装成功')
            elif max>0:
                print('安装失败!')
                max=max-1
                print("进行第"+str(4-max)+"次重试")
            else:
                break

        print("执行btfs init中...")
        command='btfs/bin/btfs init'
        stdin, stdout, stderr = client.exec_command(command)
        sleep(3)

        command='ls -a'
        stdin, stdout, stderr = client.exec_command(command)
        results = stdout.readlines()

        suc=False
        for data in results:
            if data.find('.btfs')!=-1:
                suc=True
        if suc:
            print("btfs init成功")
        else:
            print("初始化失败")
            break

        print("执行btfs config profile apply storage-host中...")
        chenggong=False
        while chenggong is False:
            command='btfs/bin/btfs config profile apply storage-host'
            stdin, stdout, stderr = client.exec_command(command)
            sleep(5)
            command=('ls .btfs/ -a')
            stdin, stdout, stderr = client.exec_command(command)
            results = stdout.readlines()
            flag=False
            for date in results:
                if date.find('config-pre-storage-host')!=-1:
                    print('执行apply成功')
                    chenggong=True

        #command=("sed -i 's/\"Initialized\": false/\"Initialized\": true/' .btfs/config")
        #print(command)
        #stdin, stdout, stderr = client.exec_command(command)
        #command=("sed -i '176d' .btfs/config")
        #print(command)
        #stdin, stdout, stderr = client.exec_command(command)
        #command=("sed -i '175a\      \"Initialized\": false' .btfs/config")
        #print(command)
        #stdin, stdout, stderr = client.exec_command(command)
        #print("修改完成")
        sleep(5)
        command=('cat .btfs/config')
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
        s1="sed -i 's/"+wri+"/"+Mnemonic_List[i+1]+"/' .btfs/config"
        print(s1)
        command=(s1)
        stdin, stdout, stderr = client.exec_command(command)
        s2="sed -i 's/"+wri1+"/"+PeerID_List[i+1]+"/' .btfs/config"
        print(s2)
        command=(s2)
        stdin, stdout, stderr = client.exec_command(command)
        s3="sed -i 's/"+wri2.replace('/','\/')+"/"+PrivKey_List[i+1].replace('/','\/')+"/' .btfs/config"
        print(s3)
        command=(s3)
        stdin, stdout, stderr = client.exec_command(command)

        command=('apt-get -y install screen')
        stdin, stdout, stderr = client.exec_command(command)
        sleep(5)

        chan = client.invoke_shell()
        chan.send('export PATH=${PATH}:${HOME}/btfs/bin\n')
        sleep(2)
        chan.send('screen -S a\n')
        sleep(3)
        chan.send('btfs daemon\n')
        sleep(5)
        print("开始后台执行。。。")
        client.close()
        sleep(3)
        print("完成")
    else:
        print("连接失败")
        sys.exit(0)
    max=0
    i=i+1
    success=False
