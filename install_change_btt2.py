'''
Author: honus
Date: 2022-02-11 15:14:39
LastEditTime: 2022-02-11 15:40:02
LastEditors: honus
Description: 
FilePath: \test\install_change_btt2.py
'''
import xlrd
import paramiko
from time import sleep
import re,os
from multiprocessing import Pool
import xlwt

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ips=table.col_values(0)[1:]
passwords=table.col_values(1)[1:]
Mnemonic_List=table.col_values(2)[1:]
PeerID_List=table.col_values(3)[1:]
PrivKey_List=table.col_values(4)[1:]

ip=ips[0]
password=passwords[0]
try_number=3

excel=xlwt.Workbook(encoding='utf-8')
tables=excel.add_sheet('result')
tables=excel.get_sheet(0)

tables.write(0, 0, 'ip')
tables.write(0, 1, 'number')
tables.write(0, 2, 'failed')
tables.write(0, 3, 'address')
begin=1

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
    print("连接失败")
    tables.write(begin, 0, ip)
    tables.write(begin, 2, 'login failed')
    begin+=1
    excel.save('./result.xls')
    os._exit(0)

for NO in range(len(Mnemonic_List)):
    command='cp -r /root/btfs /root/btfs'+str(int(NO)+1)
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()

    command='chmod +x /root/btfs/'+str(int(NO)+1)+'bin/btfs'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    chan = client.invoke_shell()
    command='export PATH=${PATH}:${HOME}/btfs'+str(int(NO)+1)+'/bin'
    chan.send(command+'\n')
    sleep(1)
    command='export BTFS_PATH=/root/.btfs'+str(int(NO)+1)
    chan.send(command+'\n')
    sleep(1)
    command='btfs init -p storage-host-testnet'
    chan.send(command+'\n')
    sleep(1)
    command='btfs daemon --chain-id 1029'
    chan.send(command+'\n')
    sleep(5)
    res=chan.recv(4096).decode()
    try:
        Bttc=re.search('the address of Bttc format is:  ([A-Za-z0-9]+)',res).group(1)
        tables.write(begin, 3, Bttc)
    except:
        print(ip + ' node '+ str(int(NO)+1) +' init error')
        tables.write(begin, 0, ip)
        tables.write(begin, 1, str(int(NO)+1))
        tables.write(begin, 2, 'init error')
        begin+=1
    chan=client.invoke_shell()
    command='export PATH=${PATH}:${HOME}/btfs'+str(int(NO)+1)+'/bin'
    chan.send(command+'\n')
    sleep(1)
    command='export BTFS_PATH=/root/.btfs'+str(int(NO)+1)
    chan.send(command+'\n')
    sleep(1)
    command='btfs config Addresses.API /ip4/127.0.0.1/tcp/'+str(int(NO)+1+5001)
    chan.send(command+'\n')
    sleep(1)
    command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/'+str(int(NO)+1+8080)
    chan.send(command+'\n')
    sleep(1)
    command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/'+str(int(NO)+1+6101)
    chan.send(command+'\n')
    sleep(1)
    command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(int(NO)+1+4001)+"\""+",\"/ip6/::/tcp/"+str(int(NO)+1+4001)+"\",\"/ip4/0.0.0.0/udp/"+str(int(NO)+1+4001)+"/quic\",\"/ip6/::/udp/"+str(int(NO)+1+4001)+"/quic\"]'"+"\n"
    #print(command)
    chan.send(command+'\n')
    sleep(1)

    command='cat .btfs'+str(NO+1)+'/config'
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    #print(res)
    PeerID='\"PeerID\": \"([a-zA-Z0-9|\+]+)\"'
    PrivKey='\"PrivKey\": \"([a-zA-Z0-9|\+|/]+)\"'
    Mnemonic='\"Mnemonic\": \"([a-zA-Z0-9| ]+)\"'

    try:
        Mnemonic=re.search(Mnemonic, res).group(1)
    except:
        tables.write(begin, 0, ip)
        tables.write(begin, 1, str(int(NO)+1))
        tables.write(begin, 2, 'Mnemonic not found')
        begin+=1
        excel.save('result.xls')
        continue
    try:
        PeerID=re.search(PeerID, res).group(1)
    except:
        tables.write(begin, 0, ip)
        tables.write(begin, 1, str(int(NO)+1))
        tables.write(begin, 2, 'PeerID not found')
        begin+=1
        excel.save('result.xls')
        continue
    try:
        PrivKey=re.search(PrivKey, res).group(1)
    except:
        tables.write(begin, 0, ip)
        tables.write(begin, 1, str(int(NO)+1))
        tables.write(begin, 2, 'PrivKey not found')
        begin+=1
        excel.save('result.xls')
        continue
    
    tables.write(begin, 0, ip)
    tables.write(begin, 1, NO+1)
    begin+=1

    Mnemonic_replace=Mnemonic_List[NO]
    PeerID_replace=PeerID_List[NO]
    PrivKey_replace=PrivKey_List[NO]

    command="sed -i 's/"+Mnemonic+"/"+Mnemonic_replace+"/' .btfs"+str(NO+1)+"/config"
    #print(command)
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    command="sed -i 's/"+PeerID+"/"+PeerID_replace+"/' .btfs"+str(NO+1)+"/config"
    #print(command)
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()
    command="sed -i 's/"+PrivKey.replace('/', '\/')+"/"+PrivKey_replace.replace('/', '\/')+"/' .btfs"+str(NO+1)+"/config"
    #print(command)
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.read().decode()

    excel.save('result.xls')
    print(str(NO+1)+' success')





