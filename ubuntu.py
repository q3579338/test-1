import paramiko
import xlrd
import xlwt
from time import sleep
from multiprocessing import Pool

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
            client.connect(ip, port= 22, username='ubuntu', password=password,timeout=30)
            return client
        except:
            if MaxTestNum > 0:
                MaxTestNum -= 1
            else:
                return False

def main(i):
    Ip = Ips[i]
    Password = Passwords[i]
    client = connect(Ip , Password)
    if client:
        print('%s connect success' % Ip)
        command = 'sudo sed -i \'s/1/0/\' /etc/apt/apt.conf.d/20auto-upgrades'
        stdin, stdout, stderr = client.exec_command(command)
        res = stdout.readlines()
        print('%s disable auto-upgrades success' % Ip)
        command = '''
        echo root:'''+ Password +''' |sudo chpasswd root
        sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/g' /etc/ssh/sshd_config;
        sudo sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/g' /etc/ssh/sshd_config;
        sudo service sshd restart
        '''
        stdin, stdout, stderr = client.exec_command(command)
        print(command)
        res = stdout.readlines()
        print('%s  change root password' % Ip)
        client.close()
        return True
    else:
        return False

if __name__ == '__main__':
    Ips = [k for k in Ips if k != '']
    Passwords = [k for k in Passwords if k != '']
    pool = Pool(processes=16)
    for i in range(len(Ips)):
        p = pool.apply_async(main, (i,))
    pool.close()
    pool.join()

