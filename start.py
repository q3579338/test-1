import os
from time import sleep

res=os.popen('ls /etc').readlines()
#print(res)
for data in res:
    if data.find('rc.local')!=-1:
        res=os.popen('cat /etc/rc.local').readlines()
        #print(res)
        for data in res:
            if data.find('startup.py')!=-1:
                print('已存在')
                os._exit(0)
            else:
                os.system('rm -rf /etc/rc.local')

os.system('wget https://raw.githubusercontent.com/0honus0/test/master/rc.local')
sleep(2)
os.system('wget https://raw.githubusercontent.com/0honus0/test/master/rc-local.service')
sleep(2)
os.system('wget https://raw.githubusercontent.com/0honus0/test/master/startup.py')
sleep(2)
os.system('mv rc-local.service /etc/systemd/system')
sleep(2)
os.system('chmod +x /etc/systemd/system/rc-local.service')
sleep(2)
os.system('mv rc.local /etc')
sleep(2)
os.system('chmod +x /etc/rc.local')
sleep(2)
os.system('systemctl enable rc-local')
sleep(2)
os.system('systemctl start rc-local.service')
sleep(3)
#os.system('reboot')

print('设置完成')