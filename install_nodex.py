import paramiko
import re,os
from time import sleep
import sys
import xlrd
import xlwt

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet('result')

for num in (range(0,len(ip_List))):
    ip=ip_List[num]
    password=password_List[num]
    max_test_number=3
    connect=False
    while max_test_number>0:
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip,22,username='root',password=password,timeout=5)
            connect=True
            break
        except:
            max_test_number-=1
            sleep(1)
            continue
    if connect:
        print("%s connect success"%ip)
        tables.write(num,0,ip)
        tables.write(num,1,password)
    else:
        print("%s connect fail"%ip+' ,begin next')
        tables.write(num,2,'connect_failed')
        continue

    #detect docker and install
    command='docker --version'
    stdin,stdout,stderr=ssh.exec_command(command)
    result=''.join(stdout.readlines())
    if 'Docker' not in result:
        command='curl -fsSL https://get.docker.com | bash'
        print('install docker')
        stdin,stdout,stderr=ssh.exec_command(command)
        result=stdout.read()
    print('docker installed')

    #detect conf and add rules
    command='cat /etc/security/limits.conf'
    stdin,stdout,stderr=ssh.exec_command(command)
    result=''.join(stdout.readlines())
    if "* hard nofile 65535" not in result:
        print('add rules to /etc/security/limits.conf')
        command='sed  -i \'$a\* soft nofile 65535\' /etc/security/limits.conf'
        stdin,stdout,stderr=ssh.exec_command(command)
        command='sed  -i \'$a\* hard nofile 65535\' /etc/security/limits.conf'
        stdin,stdout,stderr=ssh.exec_command(command)
        command='sed  -i \'$a\* soft nproc 65535\' /etc/security/limits.conf'
        stdin,stdout,stderr=ssh.exec_command(command)
        command='sed  -i \'$a\* hard nproc 65535\' /etc/security/limits.conf'
        stdin,stdout,stderr=ssh.exec_command(command)
    print('rules added')

    command='cat /etc/profile'
    stdin,stdout,stderr=ssh.exec_command(command)
    result=''.join(stdout.readlines())
    if "ulimit -SHn 65535" not in result:
        print('add rules to /etc/profile')
        command="sed -i'$a\\ulimit -SHn 65535' /etc/profile"
        stdin,stdout,stderr=ssh.exec_command(command)
        command='source /etc/profile'
        stdin,stdout,stderr=ssh.exec_command(command)
        result=stdout.readlines()
    print('rules added')

    #mkdir
    command='mkdir ~/.streamrDocker'
    stdin,stdout,stderr=ssh.exec_command(command)
    print('mkdir folder')
    result=stdout.readlines()

    #new shell to run docker
    chan=ssh.invoke_shell()
    #download image and begin setting
    command='docker run -it -v $(cd ~/.streamrDocker; pwd):/root/.streamr streamr/broker-node:testnet bin/config-wizard'
    chan.send(command+'\n')
    sleep(2)
    result=bytes.decode(chan.recv(9999))
    print(result)

    flag=False
    test=3
    while test>0:
        if 'new Ethereum private key or import an existing one' in result:
            #Generate
            chan.send('\n')
            sleep(2)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'1_failed')
        continue

    flag=False
    test=3
    while test>0:
        if 'We strongly recommend backing up your private key' in result:
            #Agree
            chan.send('y\n')
            sleep(2)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'2_failed')
        continue

    flag=False
    test=3
    while test>0:
        if 'Select the plugins to enable' in result:
            #select All plugins
            chan.send('a')
            sleep(3)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'3_failed')
        continue

    flag=False
    test=3
    while test>0:
        if 'publishHttp' in result:
            #Agree select All plugins
            chan.send('\n')
            sleep(2)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'4_failed')
        continue

    flag=False
    test=3
    while test>0:
        if '7170' in result:
            #7170 port
            chan.send('\n')
            sleep(2)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'5_failed')
        continue

    flag=False
    test=3
    while test>0:
        if '1883' in result:
            #1883 port
            chan.send('\n')
            sleep(2)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'6_failed')
        continue

    flag=False
    test=3
    while test>0:
        if '7171' in result:
            #7171 port
            chan.send('\n')
            sleep(2)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'7_failed')
        continue

    flag=False
    test=3
    while test>0:
        if 'Select a path to store the generated' in result:
            #select path for config
            chan.send('\n')
            sleep(2)
            result=bytes.decode(chan.recv(9999))
            print(result)
            flag=True
            break
        else:
            test-=1
            sleep(5)
            result=bytes.decode(chan.recv(9999))
    if not flag:
        tables.write(num,2,'8_failed')
        continue
    try:
        id=re.search('https://streamr.network/network-explorer/nodes/([\s\S]*?:)',result).group(1).replace(':','').replace('\n','')
        print(id)
        tables.write(num,2,id)
    except:
        tables.write(num,2,'get_id_failed')
        continue

    #run docker
    command='docker run -d -it -p 7170:7170 -p 7171:7171 -p 1883:1883 -v $(cd ~/.streamrDocker; pwd):/root/.streamr streamr/broker-node:testnet'
    stdin,stdout,stderr=ssh.exec_command(command)
    result=stdout.readlines()
    print('complete')
    sleep(2)
    excel.save('install_nidex_result.xls')