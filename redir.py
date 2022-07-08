import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt
import time

i=0
max_test=3
begin=0
data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')

tables=excel.get_sheet('result')
tables.write(0, 0, 'ip')
tables.write(0, 1, 'result')
PORT=9999

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
                print('连接失败，开始下一个')
                break
            else:
                print('登陆失败，尝试重新登陆')
                count +=1

    if success:
        print("连接成功")
        print("安装依赖。。。")
        command="apt-get -y install build-essential && apt -y install git && apt -y install ipset"
        stdin, stdout, stderr = client.exec_command(command)
        stdout.readlines()
        print("获取转发ip。。。")
        command='curl http://btfs.honus.top/'+ip
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        try:
            now_ip=res[0].strip('\n').strip('\"')
            pat='((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
            IP=re.search(pat,now_ip).group()
            print("转发IP为:"+str(IP))
        except:
            tables.write(i+1,0,ip)
            tables.write(i+1,1,'获取转发ip失败')
            excel.save('redir.xls')
            i+=1
            continue
        print("安装及配置ss-tproxy。。。")
        command="git clone https://github.com/zfl9/ss-tproxy && cd ss-tproxy && chmod +x ss-tproxy"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        command="cd /root/ss-tproxy && install ss-tproxy /usr/local/bin && install -d /etc/ss-tproxy && install -m 644 ss-tproxy.conf gfwlist* chnroute* ignlist* /etc/ss-tproxy && install -m 644 ss-tproxy.service /etc/systemd/system"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        command="sudo rm -rf /etc/ss-tproxy/ss-tproxy.conf && wget -P /etc/ss-tproxy/ https://raw.githubusercontent.com/0honus0/test/main/ss-tproxy.conf"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        command='sed -i "s/SERVER_IP/'+str(IP)+'/g" /etc/ss-tproxy/ss-tproxy.conf'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        command='sed -i "s/SERVER_PORT/'+str(PORT)+'/g" /etc/ss-tproxy/ss-tproxy.conf'
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        print("安装dns2tcp。。。")
        command="git clone https://github.com/zfl9/dns2tcp && cd dns2tcp && make && sudo make install"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        print("安装dnsmasq。。。")
        command="apt-get -y install dnsmasq"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        print("安装chinadns-ng。。。")
        command="git clone https://github.com/zfl9/chinadns-ng && cd chinadns-ng &&make && sudo make install"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        print("安装ipt2socks")
        command="git clone https://github.com/zfl9/ipt2socks && cd ipt2socks &&make && sudo make install"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        print("停止resolved。。。")
        command="systemctl stop systemd-resolved"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        print("启动ss-tproxy。。。")
        command="ss-tproxy start"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        print("检测是否安装成功。。。")
        command="ss-tproxy help"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        if 'Usage: ss-tproxy' in ''.join(res):
            print("开启成功")
        else:
            tables.write(i+1,0,ip)
            tables.write(i+1,1,'安装失败')
            excel.save('redir.xls')
            i+=1
            continue
        print("检测是否转发成功。。。")
        command="curl ifconfig.me"
        stdin, stdout, stderr = client.exec_command(command)
        res=stdout.readlines()
        now_ip=res[0].strip('\n').strip('\"')
        if now_ip==IP:
            print("转发成功")
        else:
            tables.write(i+1,0,ip)
            tables.write(i+1,1,'转发失败')
            excel.save('redir.xls')
            i+=1
            continue
        print('Complete')
    else:
        if row==i+1:
            break
        else:
            print("尝试下一个")
    i=i+1
