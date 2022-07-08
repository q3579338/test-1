'''
Author: honus
Date: 2022-01-25 13:23:39
LastEditTime: 2022-01-25 13:35:34
LastEditors: honus
Description: 
FilePath: \test\change_btt2_port.py
'''
import xlrd
import paramiko
from time import sleep
import re
from multiprocessing import Pool
import xlwt

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ips=table.col_values(0)
passwords=table.col_values(1)
count=len(ips)

def main(NO):
    ip=ips[NO]
    password=passwords[NO]
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
        return
    
    command='ls -a'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.readlines()

    number=0
    for i in res:
        try:
            tmp=re.search('.btfs(\d+)',i).group(1)
            if int(tmp)>number:
                number=int(tmp)
        except:
            pass

    current_number=0
    while current_number<number+1:
        print(ip+" "+str(current_number+1)+"/"+str(number))
        chan=client.invoke_shell()
        command='export PATH=${PATH}:${HOME}/btfs'+str(int(current_number)+1)+'/bin'
        chan.send(command+'\n')
        sleep(1)
        command='export BTFS_PATH=/root/.btfs'+str(int(current_number)+1)
        chan.send(command+'\n')
        sleep(1)
        command='btfs config Addresses.API /ip4/127.0.0.1/tcp/'+str(int(current_number)+1+5001)
        chan.send(command+'\n')
        sleep(1)
        command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/'+str(int(current_number)+1+8080)
        chan.send(command+'\n')
        sleep(1)
        command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/'+str(int(current_number)+1+6101)
        chan.send(command+'\n')
        sleep(1)
        command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(int(current_number)+1+4001)+"\""+",\"/ip6/::/tcp/"+str(int(current_number)+1+4001)+"\",\"/ip4/0.0.0.0/udp/"+str(int(current_number)+1+4001)+"/quic\",\"/ip6/::/udp/"+str(int(current_number)+1+4001)+"/quic\"]'"+"\n"
        #print(command)
        chan.send(command+'\n')
        sleep(1)
        current_number=int(current_number)+1
        chan.close()
    client.close()
    return content

if __name__ == '__main__':
    p=Pool(4)
    for i in range(count):
        res=p.apply_async(main,args=[i])
        print('第',str(i+1),'个进程启动.。。')
    p.close()
    p.join()
    print('所有进程运行完成')
