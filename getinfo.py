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

data=xlrd.open_workbook("D:/Study/python/data.xls",formatting_info=True)
data1=xlrd.open_workbook("D:/Study/python/alldata.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
excel=copy(data1)
#行数
row=table.nrows

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'str')

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
            print('登陆失败，尝试重新登陆')
            sleep(1)
            count +=1
            if count == max_test:
                 break
    if success:
        print("连接成功")
        # command=('df -hl')
        # stdin, stdout, stderr = client.exec_command(command)
        # results = stdout.readlines()
        # for date in results:
        #     if date.find('vda1')!=-1:
        #         shuzu=date.find('vda1')
        #         size=date[shuzu:len(date)]
        # size=size.replace(' ','')
        # reobject=re.compile('[0-9]*G')
        # size=reobject.findall(size)
        # free=size[2]
        command=('ls .btfs/ -a')
        stdin, stdout, stderr = client.exec_command(command)
        results = stdout.readlines()
        flag=False
        for date in results:
            if date.find('config-pre-storage-host')!=-1 and flag==False:
                zifu=date.find('config-pre-storage-host',0,len(date))
                flag=True
                res=date[zifu:len(date)]

        com='cat .btfs/'+res
        command=(com)
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
        tables.write(i+1, 0, ip)
        tables.write(i+1, 1, password)
        tables.write(i+1, 2, Mnemonic)
        tables.write(i+1, 3, PeerID)
        tables.write(i+1, 4, PrivKey)
        #tables.write(i+1, 5, free)
        client.close()
        excel.save('alldata.xls')
        sleep(3)
        print("完成")
    i=i+1
    success=False
