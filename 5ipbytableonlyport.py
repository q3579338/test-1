import os,re
import xlrd
import xlwt
from time import sleep
import paramiko

#1 只添加ip
#2 添加ip，修改配置文件，ip+port
mode='2'

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

if mode=='2':
    data=xlrd.open_workbook("./data.xls",formatting_info=True)
    table=data.sheets()[0]
    Ip_List=table.col_values(0)[1:]
    Password_List=table.col_values(1)[1:]
    TempIp_List=table.col_values(2)[1:]
    Port_List=table.col_values(3)[1:]

    excel = xlwt.Workbook(encoding = 'utf-8')
    tables = excel.add_sheet('result')
    tables=excel.get_sheet('result')

    count=len(Port_List)
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

        tables.write(con,3,'success')
        print('success')
        excel.save('result.xls')
        con+=1