import os,re
command='curl ifconfig.me'
ip=os.popen(command).readlines()
ip=ip[0].split('.')
lis=[]
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+1))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+2))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+3))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])+4))
lis.append(ip[0]+'.'+ip[1]+'.'+ip[2]+'.'+str(int(ip[3])))
print(lis)

#获取网卡名称
command='cat /etc/network/interfaces'
net=os.popen(command).readlines()
net=''.join(net)
net=net[20:-1]
pat='iface [\s\S]*? inet static'
result=re.search(pat,net).group()
net=result.replace('iface ','').replace(' inet','').replace(' static','')
print(net)

#检查是否添加配置文件
for i in lis:
    command='ip address add '+i+'/29 dev '+str(net)
    print(command)
    result=os.popen(command)
