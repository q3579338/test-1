'''
Author: honus
Date: 2022-03-26 15:20:22
LastEditTime: 2022-03-26 17:30:05
LastEditors: honus
Description: 
FilePath: \test\install_sds.py
'''
import paramiko
import xlrd
from multiprocessing import Pool
from time import sleep

data=xlrd.open_workbook("./data.xls",formatting_info=True)

table=data.sheets()[0]

Ips       = table.col_values(0)[1:]
PassWords = table.col_values(1)[1:]

def connect(ip,password):
    MaxTestNum = 3
    while True:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            print("%s connect success" % ip)
            return client
        except:
            if MaxTestNum > 0:
                MaxTestNum -= 1
            else:
                return False


def main(no):
    ip = Ips[no]
    password = PassWords[no]

    # Connect
    client = connect(ip,password)
    if not client:
        return False , 'connect fail'

    # Install Dependency
    # command = 'apt update && apt -y upgrade'
    # stdin, stdout, stderr = client.exec_command(command)
    # res = stdout.read()
    command = 'apt -y install git curl snapd'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.read()
    print("%s install dependency success" % ip)

    # Install Go
    command = 'source /etc/profile && go version'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.read()
    if 'go version' in res.decode('utf-8'):
        print("%s install go success" % ip)
    else:
        command = 'wget https://go.dev/dl/go1.18.linux-amd64.tar.gz'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.read()
        command = 'rm -rf /usr/local/go && tar -C /usr/local -xzf go1.18.linux-amd64.tar.gz'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.read()
        command = "sed -i '$aexport PATH=$PATH:/usr/local/go/bin' /etc/profile"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.read()
        command = "sed -i '$aexport GOROOT=/usr/local/go' /etc/profile"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.read()
        command = 'source /etc/profile && go version'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.read()
        if 'version' in res.decode('utf-8'):
            print("%s install go success" % ip)
        else:
            return False , 'install go fail'
    # command = 'go version'
    # stdin, stdout, stderr = client.exec_command(command)
    # res = stdout.read()
    # if 'version' in res.decode('utf-8'):
    #     print("%s install go success" % ip)
    # else:
    #     command = 'snap install go --classic'
    #     stdin, stdout, stderr = client.exec_command(command)
    #     res = stdout.read()
    #     print(res.decode('utf-8'))
    #     command = 'echo \'export GOPATH="$HOME/go"\' >> ~/.profile'
    #     stdin, stdout, stderr = client.exec_command(command)
    #     res = stdout.read()
    #     command = 'echo \'export PATH=$PATH:$GOPATH/bin\' >> ~/.profile'
    #     stdin, stdout, stderr = client.exec_command(command)
    #     res = stdout.read()
    #     command = 'echo \'export PATH="$GOBIN:$PATH"\' >> ~/.profile'
    #     stdin, stdout, stderr = client.exec_command(command)
    #     res = stdout.read()
    #     command = 'source ~/.profile'
    #     stdin, stdout, stderr = client.exec_command(command)
    #     res = stdout.read()
    #     print(res.decode('utf-8'))
    #     command = 'go version'
    #     stdin, stdout, stderr = client.exec_command(command)
    #     res = stdout.read()
    #     print(res.decode('utf-8'))
    #     if 'version' in res.decode('utf-8'):
    #         print("%s install go success" % ip)
    #     else:
    #         return False , 'install go fail'

    # Install SDS
    command = 'git clone https://github.com/stratosnet/sds.git'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.read()
    command = 'cd ./sds && git checkout v0.6.0 && make build'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.readlines()
    command = 'cd /root/sds && make install'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.readlines()
    # Configure SDS
    command = 'cd /root && mkdir rsnode'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.read()
    command = 'ppd'
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.read()
    print(res.decode('utf-8'))
    command = "cd rsnode && ppd config && ppd config accounts -n Wallet -p '' -s"
    stdin, stdout, stderr = client.exec_command(command)
    res = stdout.read()
    print(res.decode('utf-8'))
    sleep(999)
    # Setup SDS
    command = ''

if __name__ == '__main__':
    Ips       = [k for k in Ips if k != '']
    PassWords = [k for k in PassWords if k != '']
    for i in range(len(Ips)):
        main(i)