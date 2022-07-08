'''
Author: honus
Date: 2022-01-20 23:01:36
LastEditTime: 2022-01-21 15:51:49
LastEditors: honus
Description: 检查转账失败的节点并记录
FilePath: /test/get_btt_trans_failed.py
'''
import xlrd,xlwt,paramiko,re
from time import sleep

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ips=table.col_values(0)
passwords=table.col_values(1)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'number')
tables.write(0, 2, 'address')
tables.write(0, 3, 'status')

def main(NO):
    global begin
    global excel
    max_number=0
    ip=ips[NO]
    password=passwords[NO]

    if not ip:
        return

    try_number=3
    while try_number>0:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            print(ip+" 连接成功")
            break
        except:
            try_number-=1
    if try_number==0:
        print(ip +" 连接失败")
        tables.write(begin, 0, ip)
        tables.write(begin, 3, '连接失败')
        begin+=1

    command='ls -a'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode('utf-8')
    try:
        tmp=re.findall('.btfs(\d+)',res)
        tmp=[int(k) for k in tmp]
        max_number=max(tmp)
    except:
        pass

    if max_number==0:
        return
    
    port=6101

    for i in range(1,max_number+1):
        flag=False             #标志是否运行
        new_port=port+i
        command='netstat -ntulp |grep '+str(new_port)
        stdin, stdout, stderr = client.exec_command(command)
        sleep(1)
        res=stdout.read().decode()
        if res:
            if 'btfs' in res:
                flag=True

        if flag:
            continue
        else:
            chan=client.invoke_shell()
            command='export PATH=${PATH}:${HOME}/btfs'+str(i)+'/bin'
            chan.send(command+'\n')
            sleep(1)
            command='export BTFS_PATH=/root/.btfs'+str(i)
            chan.send(command+'\n')
            sleep(1)
            command='btfs daemon --chain-id 1029'
            chan.send(command+'\n')
            sleep(2)
            res=chan.recv(2048).decode()
            #print(res)
            if 'command' in res:
                tables.write(begin,0,ip)
                tables.write(begin,1,str(i))
                tables.write(begin,3,'node install failed')
                begin+=1
                continue
            try:
                Bttc=re.search('the address of Bttc format is:  ([A-Za-z0-9]+)',res).group(1)
            except:
                sleep(3)
                res=chan.recv(2048).decode()
                Bttc=re.search('the address of Bttc format is:  ([A-Za-z0-9]+)',res).group(1)
            print('node '+str(i)+' ' + Bttc.strip())
            tables.write(begin, 0, ip)
            tables.write(begin, 1, str(i))
            tables.write(begin, 2, Bttc)
            begin+=1
            chan.close()
            excel.save('get_trans_failed.xls')
    
if __name__ == '__main__':
    begin=1
    for i in range(len(ips)):
        main(i)