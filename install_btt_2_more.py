'''
Author: honus
Date: 2022-01-19 14:18:53
LastEditTime: 2022-01-19 19:17:15
LastEditors: honus
Description: 安装btfs 2.0 版本 多个节点
FilePath: \test\install_btfs_2_more.py
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

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'number')
tables.write(0, 2, 'address')

def main(NO):
    content=[]
    ip=ips[NO]
    password=passwords[NO]
    number=15
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

    current_number=0
    for i in res:
        try:
            tmp=re.search('.btfs(\d+)',i).group(1)
            if int(tmp)>current_number:
                current_number=int(tmp)
        except:
            pass

    if int(current_number)+1>=number:
        print(ip + ' node number is enough')
        return

    while int(current_number)+1<number:
        command='ls -a'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.read().decode()
        for i in res:
            try:
                tmp=re.search('.btfs(\d+)',i).group(1)
                if int(tmp)>current_number:
                    current_number=int(tmp)
            except:
                pass


        command='cp -r /root/btfs /root/btfs'+str(int(current_number)+1)
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.read().decode()

        command='chmod +x /root/btfs/'+str(int(current_number)+1)+'bin/btfs'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.read().decode()
        chan = client.invoke_shell()
        command='export PATH=${PATH}:${HOME}/btfs'+str(int(current_number)+1)+'/bin'
        chan.send(command+'\n')
        sleep(1)
        command='export BTFS_PATH=/root/.btfs'+str(int(current_number)+1)
        chan.send(command+'\n')
        sleep(1)
        command='btfs init -p storage-host-testnet'
        chan.send(command+'\n')
        sleep(1)
        command='btfs daemon --chain-id 1029'
        chan.send(command+'\n')
        sleep(5)
        res=chan.recv(4096).decode()
        #print(res)
        try:
            Bttc=re.search('the address of Bttc format is:  ([A-Za-z0-9]+)',res).group(1)
        except:
            print(ip + ' node '+ str(int(current_number)+1) +' init error')
            break
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
        print(ip+' node ' + str(int(current_number)+1) + ' install success,Address: '+Bttc)
        content.append((ip,int(current_number)+1,Bttc))
        current_number=int(current_number)+1
        chan.close()
    client.close()
    return content

if __name__ == '__main__':
    p=Pool(4)
    result=[]
    for i in range(count):
        res=p.apply_async(main,args=[i])
        print('第',str(i+1),'个进程启动.。。')
        result.append(res)
    p.close()
    p.join()
    index=1
    for value in result:
        value=value.get()
        if value:
            for i in value:
                tables.write(index, 0, i[0])
                tables.write(index, 1, i[1])
                tables.write(index, 2, i[2])
                index+=1
    excel.save('./result.xls')
    print('所有进程运行完成')





