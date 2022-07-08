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

time='ipv6'
print(time)
data=xlrd.open_workbook("D:/Study/python/data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('ipv6')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'lis')
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
        while lis < maxnumber+1:
            try:
                print(str(lis)+'/'+str(maxnumber))
                if lis==0:
                    command='cat .btfs/config'
                else:
                    command='cat .btfs'+str(lis)+'/config'
                #print("获取端口"+command)
                stdin, stdout, stderr = client.exec_command(command)
                res=stdout.readlines()
                duankou0=''
                for data in res:
                    pat='\"API\": \"/ip4/127.0.0.1/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou0=re.search(pat,data).group()
                        duankou0=duankou0[27:len(data)-1]
                #5001
                print('端口是'+str(duankou0))
                newport1=int(duankou0)-1000
                jieshu='1:2:3:'+str(lis+1)
                tihuan=kaishi+jieshu
                print(tihuan)
                command='cat /proc/net/dev | awk \'{i++; if(i>2){print $1}}\' | sed \'s/^[\t]*//g\' | sed \'s/[:]*$//g\''
                stdin, stdout, stderr = client.exec_command(command)
                wangka=stdout.readlines()
                #print(wangka)
                for data in wangka:
                    data=data.replace('\n','')
                    if data!='lo' and data!='':
                        wang=data
                command='ifconfig '+str(wang)+' inet6 add '+tihuan+'/64 up'
                print(command)
                stdin, stdout, stderr = client.exec_command(command)
                sleep(1)
                chan = client.invoke_shell()
                if lis==0:
                    command='export BTFS_PATH=/root/.btfs\n'
                    chan.send(command)
                    sleep(2)
                    command='export PATH=${PATH}:${HOME}/btfs/bin\n'
                    chan.send(command)
                    sleep(2)
                else:
                    command='export BTFS_PATH=/root/.btfs'+str(lis)+'\n'
                    chan.send(command)
                    sleep(2)
                    command='export PATH=${PATH}:${HOME}/btfs'+str(lis)+'/bin\n'
                    chan.send(command)
                    sleep(2)

                command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(newport1)+"\""+",\"/ip6/"+str(tihuan)+"/tcp/"+str(newport1)+"\""+"]'"+"\n"
                print(command)
                chan.send(command)
                sleep(2)
                print("完成")
                mingzi=time+".xls"
                #print(mingzi)
                excel.save(mingzi)
                begin=begin+1
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