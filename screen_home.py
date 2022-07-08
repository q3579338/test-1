import paramiko
from time import sleep

try:
    username='root'
    port= 22
    ip='127.0.0.1'
    password=''
    client=paramiko.SSHClient()
    key=paramiko.AutoAddPolicy()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port, username=username, password=password,timeout=30)
except:
    print('Failed')

command='ls'
stdin,stdout,stderr=client.exec_command(command)
res=stdout.readlines()
maxnumber=0
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
cou=1
while cou<=maxnumber:
    chan = client.invoke_shell()
    command='screen -S btfs'+str(cou)+'\n'
    chan.send(command)
    sleep(1)
    command='export BTFS_PATH=/root/.btfs'+str(cou)+'\n'
    print(command)
    chan.send(command)
    sleep(2)

    command='export PATH=${PATH}:${HOME}/btfs'+str(cou)+'/bin\n'
    print(command)
    chan.send(command)
    sleep(2)

    command='btfs daemon\n'
    print(command)
    chan.send(command)
    sleep(2)

    cou+=1

command='ls /home'
stdin,stdout,stderr=client.exec_command(command)
res=stdout.readlines()
maxnumber=0
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
cou=1
while cou<=maxnumber:
    chan = client.invoke_shell()
    command='screen -S btfs'+str(cou+128)+'\n'
    chan.send(command)
    sleep(1)
    command='export BTFS_PATH=/home/.btfs'+str(cou)+'\n'
    print(command)
    chan.send(command)
    sleep(2)

    command='export PATH=${PATH}:/home/btfs'+str(cou)+'/bin\n'
    print(command)
    chan.send(command)
    sleep(2)

    command='btfs daemon\n'
    print(command)
    chan.send(command)
    sleep(2)

    cou+=1
