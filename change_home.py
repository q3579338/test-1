import paramiko
import re,os
from time import sleep
import sys
import xlrd
import subprocess as sb

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)
row=table.nrows

i=0
max_test=3
while row > i:
    count=0
    success=False
    while count < max_test and not success:
        try:
            while ip_List[i+1]=='' or password_List[i+1]=='':
                print('完成')
                sys.exit(0)
        except:
            pass
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
                count=0
                i=i+1
                print('连接失败，开始下一个')
            else:
                print('登陆失败，尝试重新登陆')
                count =count+1
    if success:
        print("连接成功")
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
        cou=1
        port=5129
        port1=8208
        port2=6229
        port3=4129
        while cou<=maxnumber:

            # #如果不需要复制，注释下面if-else代码块
            # if cou==0:
            #     command='cp -rf /root/btfs /home/btfs'
            #     stdin,stdout,stderr=client.exec_command(command)
            #     stdout_result = stdout.readlines()
            #     print('copy success')
            # else:
            #     command='cp -rf /root/btfs'+str(cou)+' /home/btfs'+str(cou)
            #     print(command)
            #     stdin,stdout,stderr=client.exec_command(command)
            #     stdout_result = stdout.readlines()
            #     print('copy success')


            chan = client.invoke_shell()
            command='export BTFS_PATH=/root/.btfs'+str(cou)+'\n'
            print(command)
            chan.send(command)
            sleep(2)

            command='export PATH=${PATH}:${HOME}/btfs'+str(cou)+'/bin\n'
            print(command)
            chan.send(command)
            sleep(2)

            command='btfs config Addresses.API /ip4/127.0.0.1/tcp/'+str(port+cou)+'\n'
            print(command)
            chan.send(command)
            sleep(2)

            command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/'+str(port1+cou)+'\n'
            print(command)
            chan.send(command)
            sleep(2)

            command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/'+str(port2+cou)+'\n'
            print(command)
            chan.send(command)
            sleep(2)

            command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(port3+cou)+"\""+",\"/ip6/::/tcp/"+str(port3+cou)+"\""+"]'"+"\n"
            print(command)
            chan.send(command)
            sleep(2)

            cou+=1
            print('change success')
        client.close()
    else:
        print("连接失败")
    max=0
    i=i+1
    success=False