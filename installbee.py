import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt

i=0
max_test=3
begin=0

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('status')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'address')

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
            #print(password)
            print('当前在第'+str(i+1)+'个')
            #print('尝试第'+str(count+1)+'次登陆')
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
        print('登陆成功')
        command='apt-get install -y jq'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        command='wget https://github.com/ethersphere/bee/releases/download/v0.5.3/bee_0.5.3_amd64.deb'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        command='wget https://github.com/ethersphere/bee-clef/releases/download/v0.4.9/bee-clef_0.4.9_amd64.deb'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        command='sudo dpkg -i bee-clef_0.4.9_amd64.deb'
        stdin, stdout, stderr = client.exec_command(command)
        sleep(1)
        res=stdout.readlines()
        command='sudo dpkg -i bee_0.5.3_amd64.deb'
        stdin, stdout, stderr = client.exec_command(command)
        sleep(3)
        res=stdout.readlines()
        command='sudo bee-get-addr'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        try:
            addr=''.join(res).strip()
            pat='receiver=([0-9a-zA-z]*)'
            address=re.search(pat,addr).group(1)
            print(address)
            tables.write(begin+1,0,ip)
            tables.write(begin+1,1,address)
            begin+=1
            excel.save('alldata.xls')
            print('获取address成功')
        except:
            print('获取address失败')
            tables.write(begin+1,0,ip)
            begin+=1
            excel.save('alldata.xls')

    else:
        print("连接失败")
    max_test=3
    i=i+1
    success=False

#Goerli
#https://goerli.infura.io/v3/cd8135ee2e07404ab7fd85b862c01f59