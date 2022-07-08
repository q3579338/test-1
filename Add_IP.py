import os
import ipaddress

wangduan='15.235.131.128/26'

command='rm -f /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg'
os.popen(command)
command="echo 'network: {config: disabled}' > /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg"
os.popen(command)
command="rm -f /etc/netplan/50-cloud-init.yaml"
os.popen(command)
command='curl ifconfig.me'
ip=os.popen(command).readlines()
wip=ip[0]
print(wip)
command="cat /proc/net/dev | awk '{i++; if(i>2){print $1}}' | sed 's/^[\t]*//g' | sed 's/[:]*$//g'"
net=[i.strip() for i in os.popen(command).readlines()]
for i in net:
    command='ifconfig '+i
    if wip in ''.join(os.popen(command).readlines()):
        nc=i
print(nc)
command="cat /sys/class/net/"+str(nc)+"/address"
macaddress=os.popen(command).readlines()[0].strip()
txt='''network:
    version: 2
    ethernets:
        '''+str(nc)+''':
            dhcp4: true
            match:
                macaddress: '''+str(macaddress)+'''
            set-name: '''+str(nc)+'''
            addresses:
'''
all_ip=''
net = ipaddress.ip_network(wangduan)
for i in net:
    all_ip=all_ip+'                - '+str(i)+'/32\n'
all_ip+='                - '+str(wip)+'/32\n'
txt+=all_ip
print(txt)
command="echo '"+txt+"' > /etc/netplan/50-cloud-init.yaml"
os.popen(command)
command="netplan apply"
res=os.popen(command).readlines()
print(res)
