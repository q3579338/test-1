import paramiko
import xlrd
import xlwt
from time import sleep
from multiprocessing import Pool

url = 'https://github.com/bittorrent/go-btfs/releases/download/btfs-v2.1.1/btfs-linux-amd64'
version = '2.1.1'

data = xlrd.open_workbook('./data.xls',formatting_info=True)
table = data.sheets()[0]
Ips = table.col_values(0)
Passwords = table.col_values(1)

def connect(ip,password):
    MaxTestNum = 3
    while True:
        try:
            client=paramiko.SSHClient()
            key=paramiko.AutoAddPolicy()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, port= 22, username='root', password=password,timeout=30)
            return client
        except:
            if MaxTestNum > 0:
                MaxTestNum -= 1
            else:
                return False , 'connect error'

def main(i):
    Ip = Ips[i]
    Password = Passwords[i]
    client = connect(Ip , Password)
    if client:
        print('%s connect success' % Ip)
        command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = "screen -ls|awk 'NR>=2&&NR<=20{print $1}'|awk '{print \"screen -S \"$1\" -X quit\"}'|sh && pkill btfs"
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('%s success killed' % Ip)
        command = 'rm -rf btfs*'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('del btfs success')
        command = 'mkdir -p /root/btfs/bin'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('mkdir btfs success')
        command = 'wget -P /root/btfs/bin '+url
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'ls btfs/bin'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        sleep(2)
        #print(''.join(res))
        if 'btfs' in ''.join(res):
            print('download btfs success')
        else:
            return False , 'download btfs error'
        print('download btt success')
        command = 'cd btfs/bin && mv btfs-linux-amd64 btfs && chmod +x btfs'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        command = 'export PATH=${PATH}:${HOME}/btfs/bin && btfs init -p storage-host-testnet'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('init btfs success')
        command = 'echo btfs1 btfs2 btfs3 btfs4 btfs5 btfs6 btfs7 btfs8|xargs -n1 cp -r btfs'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('copy btfs success')
        command = 'rm -f auto_btt_test.py && wget https://raw.githubusercontent.com/0honus0/test/main/auto_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('download auto_btt_test.py success')
        command = 'screen -Sdm RUN2.2 python3 auto_btt_test.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('run auto_btt_test.py success')
        command = 'rm -f monit.py && wget https://raw.githubusercontent.com/0honus0/test/main/monit.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('download monit.py success')
        command = 'screen -Sdm monitor2.4 python3 monit.py'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('run monit.py success')
        command = 'export PATH=${PATH}:${HOME}/btfs/bin && btfs version'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        #print(res)
        res = res[0].split(' ')[-1].strip()
        #print(res)
        client.close()
        if version in res:
            return True , 'success'
        else:
            return False , 'btfs version error'
    else:
        return False , 'connect error'

if __name__ == '__main__':
    excel = xlwt.Workbook(encoding = 'utf-8')
    tables = excel.add_sheet('result')
    tables=excel.get_sheet(0)
    tables.write(0, 0, 'Ip')
    tables.write(0, 1, 'Password')
    tables.write(0, 2, 'Result')
    flag = 1
    res = []
    Ips = [k for k in Ips if k != '']
    Passwords = [k for k in Passwords if k != '']
    pool = Pool(processes=16)
    for i in range(len(Ips)):
        p = pool.apply_async(main, (i,))
        res.append(p)
    pool.close()
    pool.join()
    for k in range(len(res)):
        value = res[k].get()
        #print(value)
        if not value[0]:
            tables.write(flag, 0, Ips[k])
            tables.write(flag, 1, Passwords[k])
            tables.write(flag, 2, value[1])
            flag += 1
        excel.save('./result.xls')