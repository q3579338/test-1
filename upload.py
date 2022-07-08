import paramiko
import re,os,json
from time import sleep
import sys,random
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
tables.write(0, 3, 'hash')
tables.write(0, 4, 'id')



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
                excel.save('upload.xls')
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
            chan=client.invoke_shell()
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
            if lis==0:
                command='cat .btfs/config'
            else:
                command='cat .btfs'+str(lis)+'/config'
            stdin, stdout, stderr = client.exec_command(command)
            res=stdout.readlines()

            duankou0=''
            for data in res:
                    pat='\"API\": \"/ip4/127.0.0.1/tcp/[0-9]*'
                    if re.search(pat,data)!=None:
                        duankou0=re.search(pat,data).group()
                        duankou0=duankou0[27:len(data)-1]
            print(duankou0)
m
            daxiao=random.randint(10,50)
            print(daxiao)
            if lis==0:
                command='dd if=/dev/urandom of=/root/upload_file bs=1M count='+str(daxiao)
            else:
                command='dd if=/dev/urandom of=/root/upload'+str(lis)+'_file bs=1M count='+str(daxiao)
            print(command)
            stdin, stdout, stderr = client.exec_command(command)
            sleep(20)
            print('随机文件生成')
            if lis==0:
                command='curl -X POST -F file=@upload_file "http://localhost:'+str(duankou0)+'/api/v1/add?chunker=reed-solomon"'
            else:
                command='curl -X POST -F file=@upload'+str(lis)+'_file "http://localhost:'+str(duankou0)+'/api/v1/add?chunker=reed-solomon"'
            print(command)
            stdin, stdout, stderr = client.exec_command(command)
            res=stdout.readlines()
            #print(res)
            res=json.loads(res[0])
            hs=res['Hash']
            print(hs)
            #print(res['Size'])
            # command='curl -X POST "http://localhost:5001/api/v1/storage/upload?arg='+str(hs)+'&price=1&storage-length=35"'
            # stdin, stdout, stderr = client.exec_command(command)
            # res=stdout.readlines()
            # ID=json.loads(res[0])['ID']
            # print(ID)
            tables.write(begin,0,ip)
            tables.write(begin,1,password)
            tables.write(begin,2,lis)
            tables.write(begin,3,hs)
            #tables.write(begin,4,ID)
            begin+=1
            lis=lis+1
            excel.save('upload.xls')
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    if row+1!=maxnumber:
        i=i+1
