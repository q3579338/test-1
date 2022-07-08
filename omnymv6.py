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
maxnumber=10   #如果第一次运行，创建个数为maxnumber+1个。如果第二次运行。创建个数为maxnumber+2
begin=0

#添加ipv6
#ifconfig eno1 inet6 add 2a01:4f9:4b:14ce::3/64 up
#删除ipv6
#ifconfig enp4s0f3 inet6 del 8888::a99/96

time='nym'
data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('nym')

tables=excel.get_sheet(0)
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

        command='ls'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        lis=0
        for data in res:
            #print(data)
            geshu=data.find('nym-mixnode_linux_x86_64')
            shu=data.replace('nym-mixnode_linux_x86_64','').replace('\n','')
            if geshu!=-1:
                if shu=='':
                    shu=0
                else:
                    shu=int(shu.replace('_',''))
                if shu > lis:
                    lis=shu
        #print(lis)

        ipv6=''
        command='ip addr show'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        for data in res:
            pat='inet6 ([^f:][\da-f:]+)/(\d+) scope global'
            if re.search(pat,data)!=None:
                ipv6=re.search(pat,data).group()
                ipv6=ipv6.replace('inet6 ','').replace('/64 scope global','')
        pat='[A-Za-z0-9]+:[A-Za-z0-9]+:[A-Za-z0-9]+:[A-Za-z0-9]+:'
        kaishi=re.search(pat,ipv6).group()
        #print(kaishi)
        port=1789
        while lis < maxnumber+1:
            try:
                print('进度:'+str(lis)+'/'+str(maxnumber))
                cunzai=False
                command='ls'
                stdin, stdout, stderr = client.exec_command(command)
                res=stdout.readlines()
                data=''.join(res)
                if data.find('nym-mixnode_linux_x86_64')!=-1:
                    cunzai=True
                if lis==0 and not cunzai:
                    command='apt -y install screen'
                    stdin, stdout, stderr = client.exec_command(command)
                    jieshu='3:2:1:'+str(lis+1)
                    tihuan=kaishi+jieshu
                    print(tihuan)
                    command='ifconfig eno1 inet6 add '+tihuan+'/64 up'
                    print(command)
                    stdin, stdout, stderr = client.exec_command(command)
                    sleep(1)
                    command='wget https://github.com/nymtech/nym/releases/download/v0.9.2/nym-mixnode_linux_x86_64'
                    print(command)
                    stdin, stdout, stderr = client.exec_command(command)
                    sleep(1)
                    command='chmod +x nym-mixnode_linux_x86_64'
                    print(command)
                    stdin, stdout, stderr = client.exec_command(command)
                    command='./nym-mixnode_linux_x86_64 init --id nym'+str(lis)+' --host '+tihuan+' --port 1789 --incentives-address VJL5tRr66vFVw7tkUpKKheYFGa8oLQawSeRPYtiEJdZyxxE1E6hZA4AU6KcokS8Hcixtq1gAeyKfMBRy'
                    print(command)
                    stdin, stdout, stderr = client.exec_command(command)
                    sleep(8)
                    command='ls /root/.nym/mixnodes'
                    stdin, stdout, stderr = client.exec_command(command)
                    res=stdout.readlines()
                    find=False
                    pat='nym'+str(lis)
                    print(pat)
                    for data in res:
                        if data.find(pat)!=-1 and find is False:
                            find=True
                    if find is False:
                        print('init失败!!!')
                        tables.write(begin+1,0,ip)
                        tables.write(begin+1,1,lis)
                        tables.write(begin+1, 2, 'init失败')
                        begin=begin+1
                        mingzi=time+".xls"
                        excel.save(mingzi)
                    else:
                        print('init成功')
                    chan = client.invoke_shell()
                    chan.send('screen -S nym'+str(lis)+'\n')
                    sleep(2)
                    command='./nym-mixnode_linux_x86_64 run --id nym'+str(lis)+'\n'
                    print(command)
                    chan.send(command)
                    sleep(2)

                else:
                    if lis==0:
                        command='cp nym-mixnode_linux_x86_64 nym-mixnode_linux_x86_64_1'
                        stdin, stdout, stderr = client.exec_command(command)
                        flag=1
                    elif lis==1:
                        comand='ls'
                        stdin, stdout, stderr = client.exec_command(command)
                        res=stdout.readlines()
                        data=''.join(res)
                        if data.find('nym-mixnode_linux_x86_64_1')==-1:
                            command='cp nym-mixnode_linux_x86_64 nym-mixnode_linux_x86_64_1'
                            stdin, stdout, stderr = client.exec_command(command)
                            flag=0
                        else:
                            command='cp nym-mixnode_linux_x86_64_1 nym-mixnode_linux_x86_64_2'
                            stdin, stdout, stderr = client.exec_command(command)
                            flag=1

                    else:
                        comand='ls'
                        stdin, stdout, stderr = client.exec_command(command)
                        res=stdout.readlines()
                        data=''.join(res)
                        if data.find('nym-mixnode_linux_x86_64_'+str(lis))==-1:
                            command='cp nym-mixnode_linux_x86_64_'+str(lis-1)+' nym-mixnode_linux_x86_64_'+str(lis)
                            stdin, stdout, stderr = client.exec_command(command)
                            flag=0
                        else:
                            command='cp nym-mixnode_linux_x86_64_'+str(lis)+' nym-mixnode_linux_x86_64_'+str(lis+1)
                            stdin, stdout, stderr = client.exec_command(command)
                            flag=1
                    if flag==0:
                        jieshu='3:2:1:'+str(lis+1)
                        tihuan=kaishi+jieshu
                        print(tihuan)
                        command='ifconfig eno1 inet6 add '+tihuan+'/64 up'
                        stdin, stdout, stderr = client.exec_command(command)
                        print(command)
                        sleep(1)
                        stdin, stdout, stderr = client.exec_command(command)
                        command='ls -a'
                        stdin, stdout, stderr = client.exec_command(command)
                        res=stdout.readlines()
                        find=False
                        pat='nym-mixnode_linux_x86_64_'+str(lis)
                        print(pat)
                        for data in res:
                            if data.find(pat)!=-1 and find is False:
                                find=True
                        if find is False:
                            print('copy失败!!!')
                            tables.write(begin+1,0,ip)
                            tables.write(begin+1,1,lis)
                            tables.write(begin+1, 2, 'copy失败')
                            begin=begin+1
                            mingzi=time+".xls"
                            excel.save(mingzi)
                        else:
                            print('copy成功')
                        command='./nym-mixnode_linux_x86_64 init --id nym'+str(lis)+' --host '+tihuan+' --port '+str(int(port)+int(lis))+' --incentives-address VJL5tRr66vFVw7tkUpKKheYFGa8oLQawSeRPYtiEJdZyxxE1E6hZA4AU6KcokS8Hcixtq1gAeyKfMBRy'
                        stdin, stdout, stderr = client.exec_command(command)
                        sleep(10)
                        command='ls /root/.nym/mixnodes'
                        stdin, stdout, stderr = client.exec_command(command)
                        res=stdout.readlines()
                        find=False
                        pat='nym'+str(lis)
                        print(pat)
                        for data in res:
                            if data.find(pat)!=-1 and find is False:
                                find=True
                        if find is False:
                            print('init失败!!!')
                            tables.write(begin+1,0,ip)
                            tables.write(begin+1,1,lis)
                            tables.write(begin+1, 2, 'init失败')
                            begin=begin+1
                            mingzi=time+".xls"
                            excel.save(mingzi)
                        else:
                            print('init成功')
                        chan = client.invoke_shell()
                        command='screen -S nym'+str(lis)+'\n'
                        chan.send(command)
                        print(command)
                        sleep(2)
                        command='./nym-mixnode_linux_x86_64_'+str(lis)+' run --id nym'+str(lis)+'\n'
                        print(command)
                        chan.send(command)
                        sleep(2)
                        print('开始后台运行...')
                    else:
                        jieshu='3:2:1:'+str(lis+2)
                        tihuan=kaishi+jieshu
                        print(tihuan)
                        command='ifconfig eno1 inet6 add '+tihuan+'/64 up'
                        stdin, stdout, stderr = client.exec_command(command)
                        print(command)
                        sleep(1)
                        stdin, stdout, stderr = client.exec_command(command)
                        command='ls -a'
                        stdin, stdout, stderr = client.exec_command(command)
                        res=stdout.readlines()
                        find=False
                        pat='nym-mixnode_linux_x86_64_'+str(lis+1)
                        print(pat)
                        for data in res:
                            if data.find(pat)!=-1 and find is False:
                                find=True
                        if find is False:
                            print('copy失败!!!')
                            tables.write(begin+1,0,ip)
                            tables.write(begin+1,1,lis)
                            tables.write(i+1, 2, 'copy失败')
                            begin=begin+1
                            mingzi=time+".xls"
                            excel.save(mingzi)
                        else:
                            print('copy成功')
                        command='./nym-mixnode_linux_x86_64 init --id nym'+str(lis+1)+' --host '+tihuan+' --port '+str(int(port)+int(lis+1))+' --incentives-address VJL5tRr66vFVw7tkUpKKheYFGa8oLQawSeRPYtiEJdZyxxE1E6hZA4AU6KcokS8Hcixtq1gAeyKfMBRy'
                        print(command)
                        stdin, stdout, stderr = client.exec_command(command)
                        sleep(8)
                        command='ls /root/.nym/mixnodes'
                        stdin, stdout, stderr = client.exec_command(command)
                        res=stdout.readlines()
                        find=False
                        pat='nym'+str(lis+1)
                        print(pat)
                        for data in res:
                            if data.find(pat)!=-1 and find is False:
                                find=True
                        if find is False:
                            print('init失败!!!')
                            tables.write(begin+1,0,ip)
                            tables.write(begin+1,1,lis)
                            tables.write(begin+1, 2, 'init失败')
                            begin=begin+1
                            mingzi=time+".xls"
                            excel.save(mingzi)
                        else:
                            print('init成功')
                        chan = client.invoke_shell()
                        command='screen -S nym'+str(lis+1)+'\n'
                        chan.send(command)
                        print(command)
                        sleep(2)
                        command='./nym-mixnode_linux_x86_64_'+str(lis+1)+' run --id nym'+str(lis+1)+'\n'
                        print(command)
                        chan.send(command)
                        sleep(2)
                        print('开始后台运行...')
                lis=lis+1
            except:
                tables.write(begin+1,0,ip)
                tables.write(begin+1,1,lis)
                tables.write(begin+1,2,'runInterrupt')
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