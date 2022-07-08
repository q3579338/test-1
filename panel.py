import paramiko
import requests
import json
import random
import string
import re
import xlrd
from time import sleep
data=xlrd.open_workbook("./all.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
name_List=table.col_values(2)
row=table.nrows

i=0
max_test=3

while i<row:
    count=0
    success=False
    while count < max_test and not success:
        try:
            username='root'
            port= 22
            ip=ip_List[i]
            password=password_List[i]
            name=name_List[i]
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
            if count == max_test-1:
                i=i+1
                count=0
                print('连接失败，开始下一个')
                break
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print('连接成功')
        url='http://209.126.9.94/api/server'
        cookies={'nezha-dashboard': '149e68864049645374530c604e38184d'}
        data={"name":name}
        res=requests.post(url=url,cookies=cookies,data=json.dumps(data))
        res=json.loads(res.text)
        if str(res['code'])!='200':
            print('cookies失效')
            break
        url='http://209.126.9.94/server'
        res=requests.get(url=url,cookies=cookies).text
        code=res.find(name)
        code=res[code+20:code+200].split()
        code=code[2].replace('<td>','').replace('</td>','')
        command='mkdir -p /opt/nezha/agent'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        sleep(1)
        command='chmod 777 -R /opt/nezha/agent'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        sleep(1)

        flag=False
        while not flag:
            command='wget -O nezha-agent_linux_amd64.tar.gz https://github.com/naiba/nezha/releases/latest/download/nezha-agent_linux_amd64.tar.gz >/dev/null 2>&1'
            print(command)
            stdin,stdout,stderr=client.exec_command(command)
            command='ls'
            stdin,stdout,stderr=client.exec_command(command)
            res=stdout.readlines()
            for k in res:
                if 'nezha-agent_linux_amd64.tar.gz' in k:
                    flag=True
        print('下载完成')
        command='tar xf nezha-agent_linux_amd64.tar.gz && mv nezha-agent /opt/nezha/agent && rm -rf README.md'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        sleep(2)
        command='wget -O /etc/systemd/system/nezha-agent.service https://raw.githubusercontent.com/naiba/nezha/master/script/nezha-agent.service >/dev/null 2>&1'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        sleep(2)
        command='sed -i "s/nz_grpc_host/209.126.9.94/" /etc/systemd/system/nezha-agent.service'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        command='sed -i "s/nz_grpc_port/5555/" /etc/systemd/system/nezha-agent.service'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        command='sed -i "s/nz_client_secret/'+str(code)+'/" /etc/systemd/system/nezha-agent.service'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        command='systemctl daemon-reload'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        sleep(2)
        command='systemctl enable nezha-agent'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        sleep(2)
        command='systemctl restart nezha-agent'
        print(command)
        stdin,stdout,stderr=client.exec_command(command)
        sleep(3)
        client.close()
        print('完成')
    i=i+1

