import os,re
import xlrd
import xlwt
from time import sleep
import paramiko

def invoke_shell(chan,command):
    print(command)
    chan.send(command)
    sleep(1)
    return bytes.decode(chan.recv(9999))

def add_temp_ip(client,ip,tempip):
    command="cat /proc/net/dev | awk '{i++; if(i>2){print $1}}' | sed 's/^[\t]*//g' | sed 's/[:]*$//g'"
    stdin, stdout, stderr = client.exec_command(command)
    res=stdout.readlines()
    net=[i.strip() for i in res]
    for i in net:
        command='ifconfig '+i
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        if ip in ''.join(res):
            nc=i
    print('network card: '+str(nc))

    command='ip address add '+tempip+' dev '+str(nc)
    stdin,stdout,stderr=client.exec_command(command)
    res=stdout.readlines()

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
Ip_List=table.col_values(0)[1:]
Password_List=table.col_values(1)[1:]
TempIp_List=table.col_values(2)[1:]
Port_List=table.col_values(3)[1:]
Mnemonic_List=table.col_values(4)[1:]
PeerID_List=table.col_values(5)[1:]
PrivKey_List=table.col_values(6)[1:]

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet('result')

count=len(Mnemonic_List)
API_Port=5001
Gateway_Port=8080
RemoteAPI_Port=6101
con=0
while con<count:
    if Ip_List[con]!="":
        #connect to vps
        ip=Ip_List[con].strip()
        port=22
        print(ip)
        password=Password_List[con]
        print(password)
        max_test_number=3
        connect=False
        while max_test_number>0:
            try:
                ssh=paramiko.SSHClient()
                key=paramiko.AutoAddPolicy()
                ssh.set_missing_host_key_policy(key)
                ssh.connect(ip, port, username='root', password=password,timeout=10)
                connect=True
                break
            except:
                max_test_number-=1
                print('connext failed,test again')
                sleep(1)

        if connect:
            print("%s connect success"%ip)
            tables.write(con,0,ip)
            tables.write(con,1,password)
            tables.write(con,2,con+1)
        else:
            print("%s connect fail"%ip+' ,begin next')
            tables.write(con,3,'connect failed')
            con+=1
            excel.save('./result.xls')
            continue
    if Ip_List[con]=='' and not connect:
        con+=1
        continue
    if Ip_List[con]=='' and connect:
        tables.write(con,0,ip)
        tables.write(con,1,password)
        tables.write(con,2,con+1) 

    tempip=TempIp_List[con]
    port=Port_List[con]
    mnemonic=Mnemonic_List[con]
    peerid=PeerID_List[con]
    privkey=PrivKey_List[con]

    #copy btfs
    command='cp -r btfs btfs'+str(con+1)
    print(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    sleep(2)
    command='ls -a'
    stdin, stdout, stderr = ssh.exec_command(command)
    res=stdout.readlines()
    find=False
    pat='btfs'+str(con+1)
    for data in res:
        if data.find(pat)!=-1 and find is False:
            find=True
    if find is False:
        print('copy失败!!!')
        tables.write(con, 3, 'copy failed')
        con+=1
        continue
    else:
        print('copy success')
    sleep(2)

    suc=False
    test_test=3
    while suc is False and (test_test != 0):
        chan = ssh.invoke_shell()
        command='export BTFS_PATH=/root/.btfs'+str(con+1)+'\n'
        chan.send(command)
        sleep(1)
        command='export PATH=${PATH}:${HOME}/btfs'+str(con+1)+'/bin\n'
        chan.send(command)
        sleep(1)
        chan.send('btfs init\n')
        sleep(2)
        command='ls -a'
        stdin, stdout, stderr = ssh.exec_command(command)
        results = stdout.readlines()

        for data in results:
            pat='.btfs'+str(con+1)
            if data.find(pat)!=-1:
                suc=True
        if suc:
            print("btfs"+str(con+1)+" init success")
        elif test_test!=0:
            print("init failed ,test again")
            test_test=test_test-1
        elif test_test==0:
            tables.write(con, 3, 'init failed')
            print('init failed')
            break
        sleep(2)
    if not suc:
        con+=1
        continue

    chenggong=False
    te=3
    while chenggong is False and te>0:
        chan.send('btfs config profile apply storage-host\n')
        sleep(5)
        print("btfs config profile apply storage-host...")
        command=('ls .btfs'+str(con+1)+'/ -a')
        stdin, stdout, stderr = ssh.exec_command(command)
        results = stdout.readlines()
        flag=False
        for date in results:
            if date.find('config-pre-storage-host')!=-1:
                print('apply success')
                chenggong=True
        te=te-1
    if not chenggong:
        tables.write(con, 3, 'apply failed')
        con+=1
        continue

    #add tempip to vps
    command='apt -y install net-tools'
    stdin, stdout, stderr = ssh.exec_command(command)
    results = stdout.readlines()
    add_temp_ip(ssh,ip,tempip)

    #begin change config
    chan=ssh.invoke_shell()

    command='export BTFS_PATH=/root/.btfs'+str(con+1)+'\n'
    invoke_shell(chan,command)
    command='export PATH=${PATH}:${HOME}/btfs'+str(con+1)+'/bin\n'
    invoke_shell(chan,command)
    command='btfs config Addresses.API /ip4/'+str(tempip)+'/tcp/'+str(API_Port+con)+'\n'
    invoke_shell(chan,command)
    command='btfs config Addresses.Gateway /ip4/'+str(tempip)+'/tcp/'+str(Gateway_Port+con)+'\n'
    invoke_shell(chan,command)
    command='btfs config Addresses.RemoteAPI /ip4/'+str(tempip)+'/tcp/'+str(RemoteAPI_Port+con)+'\n'
    invoke_shell(chan,command)
    command="btfs config --json Addresses.Swarm '[\"/ip4/"+str(tempip)+"/tcp/"+str(int(port))+"\""+",\"/ip4/"+str(tempip)+"/udp/"+str(int(port))+"/quic\"]'"+"\n"
    invoke_shell(chan,command)

    #change three config
    command='cat .btfs'+str(con+1)+'/config'
    stdin, stdout, stderr = ssh.exec_command(command)
    results = stdout.readlines()
    find=False
    find1=False
    find2=False
    for data in results:
        while  data.find("PeerID",0,len(data))!=-1 and find1==False:
            zifu1=data.find("PeerID",0,len(data))
            find1=True
            wri1=data[zifu1+10:len(data)-3]
            print(wri1)
    for data in results:
        while  data.find("PrivKey",0,len(data))!=-1 and find2==False:
            zifu2=data.find("PrivKey",0,len(data))
            find2=True
            wri2=data[zifu2+11:len(data)-2]
            print(wri2)
    for data in results:
        while  data.find("Mnemonic",0,len(data))!=-1 and find==False:
            zifu=data.find("Mnemonic",0,len(data))
            find=True
            wri=data[zifu+12:len(data)-3]
            print(wri)
    s1="sed -i 's/"+wri+"/"+str(mnemonic)+"/' .btfs"+str(con+1)+"/config"
    print(s1)
    command=(s1)
    stdin, stdout, stderr = ssh.exec_command(command)
    s2="sed -i 's/"+wri1+"/"+str(peerid)+"/' .btfs"+str(con+1)+"/config"
    print(s2)
    command=(s2)
    stdin, stdout, stderr = ssh.exec_command(command)
    s3="sed -i 's/"+wri2.replace('/','\/')+"/"+str(privkey).replace('/','\/')+"/' .btfs"+str(con+1)+"/config"
    print(s3)
    command=(s3)
    stdin, stdout, stderr = ssh.exec_command(command)

    tables.write(con,3,'success')
    print('success')
    excel.save('result.xls')
    con+=1

