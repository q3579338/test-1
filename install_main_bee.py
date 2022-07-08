import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
import time

password=''
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
tables = excel.add_sheet('status')

tables=excel.get_sheet('status')
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'status')


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
                tables.write(begin+1,2,'loginfailed')
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
        command='apt -y install wget'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        commad='sudo apt -y install curl'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='rm -rf bee-clef_0.6.0_amd64.deb'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='rm -rf bee_1.0.1-rc1_amd64.deb'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('rm...')
        command='wget https://github.com/ethersphere/bee-clef/releases/download/v0.6.0/bee-clef_0.6.0_amd64.deb'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('download...')
        chan = client.invoke_shell()
        command='sudo dpkg -i bee-clef_0.6.0_amd64.deb'
        chan.send(command+'\n')
        sleep(3)
        result=bytes.decode(chan.recv(4096))
        # stdin,stdout,stderr=client.exec_command(command)
        # res=stdout.readlines()
        print('install...')
        command='wget https://github.com/ethersphere/bee/releases/download/v1.0.1-rc1/bee_1.0.1-rc1_amd64.deb'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('download...')
        chan = client.invoke_shell()
        command='sudo dpkg -i bee_1.0.1-rc1_amd64.deb'
        chan.send(command+'\n')
        sleep(3)
        result=bytes.decode(chan.recv(4096))
        # stdin,stdout,stderr=client.exec_command(command)
        # res=stdout.readlines()
        print('install...')
        command='systemctl stop bee'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('stop...')
        command='mv /etc/bee/bee.yaml /etc/bee/bee.yaml.bak'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('mv....')
        command='echo "clef-signer-enable: true" > /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "clef-signer-endpoint: /var/lib/bee-clef/clef.ipc" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "config: /etc/bee/bee.yaml" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "data-dir: /var/lib/bee" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "mainnet: true" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "network-id: 1" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "full-node: true" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "password-file: /var/lib/bee/password" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "swap-endpoint: http://162.55.2.33:8545" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "db-open-files-limit: 2000" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='curl ifconfig.me'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        ip=res[0]
        key='echo "nat-addr: \\"'+str(ip)+':1634\\"" >> /etc/bee/bee.yaml'
        command=key
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "debug-api-enable: true" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        command='echo "debug-api-addr: 127.0.0.1:1635" >> /etc/bee/bee.yaml'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('echo...')
        # chan = client.invoke_shell()
        # print('+++++++++')
        # chan.send('/usr/bin/bee start --config /etc/bee/bee.yaml\n')
        # sleep(2)
        # result=bytes.decode(chan.recv(4096))
        # print(result)
        # chan.send(password+'\n')
        # sleep(2)
        # result=bytes.decode(chan.recv(4096))
        # print(result)
        # chan.send(password+'\n')
        # sleep(2)
        # result=bytes.decode(chan.recv(4096))
        # print(result)
        command='systemctl restart bee'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        print('restart....')
        print('Complete')
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    if row+1!=maxnumber:
        i=i+1
