import os
import paramiko
import xlrd
import xlwt
from multiprocessing import Pool
from time import sleep

min_data = 200

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

Ips = table.col_values(0)
Passwords = table.col_values(1)

flag = 1
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'password')
tables.write(0, 2, 'status')

def connect(ip,password):
    try:
        client=paramiko.SSHClient()
        key=paramiko.AutoAddPolicy()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port= 22, username='root', password=password,timeout=30)
        print(f"{ip} 连接成功")
        return client
    except:
        return False

def del_btfs(client , Ip , Password):
    command='ls'
    stdin,stdout,stderr=client.exec_command(command)
    res=stdout.readlines()
    
    MaxNumber = 0
    for data in res:
        geshu=data.find('btfs')
        shu=data.replace('btfs','').replace('\n','')
        if geshu!=-1:
            if shu=='':
                shu=0
            else:
                shu=int(shu)
            if shu > MaxNumber:
                MaxNumber = shu

    data = []
    #获取少于200M占用的btfs
    for i in range(1 , MaxNumber+1):
        command = 'du -s .btfs' + str(i)
        stdin,stdout,stderr=client.exec_command(command)
        res = stdout.readlines()
        if len(res) == 0:
            command = f"rm -rf btfs{i}"
            stdin,stdout,stderr=client.exec_command(command)
            res = stdout.readlines()
            continue
        storage_used = int(res[0].strip().split('\t')[0])/1024        #M
        btfs_name = int(res[0].strip().split('\t')[1].replace('.btfs',''))
        if storage_used < min_data:
            data.append((storage_used , btfs_name))

    print( f"{Ip} 共有 {len(data)} 台数据占用少于200M")

    # if len(data) == 0:
    #     return

    #删除少于200M的btfs
    for i in data:
        command = f"rm -rf .btfs{i[1]} btfs{i[1]}"
        stdin,stdout,stderr=client.exec_command(command)
        res = stdout.read()

    #获取剩余btfs索引并重命名
    command = 'ls'
    stdin,stdout,stderr=client.exec_command(command)
    res = stdout.readlines()
    tmp = []
    for i in res:
        if 'btfs' in i:
            i = i.strip().replace('btfs' , '')
            if i:
                tmp.append(int(i))
    tmp.sort()
    key = 1
    for i in tmp:
        command = f"mv btfs{i} btfs{key} && mv .btfs{i} .btfs{key}"
        stdin,stdout,stderr=client.exec_command(command)
        key+=1
                
    #修改端口
    chan = client.invoke_shell()
    for i in range(1,key):
        print(f"进度 : {i}/{key-1}")
        API_Port       = 5001 + i
        Gateway_Port   = 8080 + i
        RemoteAPI_Port = 6101 + i
        Swarm_Port     = 4001 + i
        command = f"export BTFS_PATH=/root/.btfs{i}\n"
        print(command.strip())
        chan.send(command)
        sleep(1)
        command = f"export PATH=${{PATH}}:${{HOME}}/btfs{i}/bin\n"
        print(command.strip())
        chan.send(command)
        sleep(1)
        command = f"btfs config Addresses.API /ip4/127.0.0.1/tcp/{API_Port}\n"
        print(command.strip())
        chan.send(command)
        sleep(2)
        command = f"btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/{Gateway_Port}\n"
        print(command.strip())
        chan.send(command)
        sleep(2)
        command = f"btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/{RemoteAPI_Port}\n"
        print(command.strip())
        chan.send(command)
        sleep(2)
        command = f"btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/{Swarm_Port}\",\"/ip6/::/tcp/{Swarm_Port}\"]'\n"
        print(command.strip())
        chan.send(command)
        sleep(2)
    print(f"{Ip} 完成")

def main(no):
    global flag
    Ip = Ips[no]
    Password = Passwords[no]

    res = connect(Ip , Password)

    if not res:
        tables.write(flag , 0 , Ip)
        tables.write(flag , 1 , Password)
        tables.write(flag , 2 , 'connect failed')
        flag+=1
        return
    
    del_btfs(res , Ip , Password)


if __name__ == '__main__':
    Ips = [key for key in Ips if key != '']
    Passwords = [key for key in Passwords if key != '']
    for i in range(len(Ips)):
        main(i)
        excel.save('res.xls')
