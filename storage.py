import paramiko
import re,os,json
from time import sleep
import sys
import xlrd
import xlwt
from xlutils.copy import copy
import time

i=0
max_test=3
maxnumber=0
begin=1

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('storage')

tables=excel.get_sheet('storage')
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'n')
tables.write(0, 3, 'check')



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
                tables.write(begin,0,ip)
                tables.write(begin,1,password)
                tables.write(begin,3,'loginfailed')
                excel.save('storage.xls')
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
        while lis <= maxnumber:
            try:
                print(str(lis)+'/'+str(maxnumber))
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
                chan.send('btfs storage announce -s 1\n')
                sleep(2)
                chan.send('btfs storage info\n')
                sleep(3)            #最小2
                result=bytes.decode(chan.recv(1024))
                pat='info[\s\S]*}'
                data=re.search(pat,result).group(0)
                data=json.loads(data.strip('info\r\n'))
                #print(data['storage_price_ask'])
                if data['storage_price_ask']!=1:
                    tables.write(begin,0,ip)
                    tables.write(begin,1,password)
                    tables.write(begin,2,begin)
                    tables.write(begin,3,'storage_announce_failed')
                    begin+=1
                    excel.save('storage.xls')
                lis=lis+1
            except:
                print('执行失败')
                tables.write(begin,0,ip)
                tables.write(begin,1,password)
                tables.write(begin,2,begin)
                tables.write(begin,3,'storage_announce_failed')
                begin+=1
                lis=lis+1
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    if row+1!=maxnumber:
        i=i+1
