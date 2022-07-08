import os,re
from time import sleep

command='curl icanhazip.com'
res=os.popen(command)
ip=res.read()
if ip=='':
    os._exit(0)
ip=ip.strip('\n')
command='curl btfs.honus.top/'+ip
res=os.popen(command)
proxy=res.read()
if proxy=='':
    os._exit(0)
if proxy=='False':
    os._exit(0)
proxy=proxy.strip('\n').strip('\"')
print(proxy)

lis=0
if lis==0:
    os.environ['BTFS_PATH'] = '/root/.btfs'
else:
    com='/root/.btfs'+str(lis)
    print(com)
    os.environ['BTFS_PATH'] = com
if lis==0:
    os.environ['PATH'] = '${PATH}:${HOME}/btfs/bin'
else:
    com='${PATH}:${HOME}/btfs'+str(lis)+'/bin'
    print(com)
    os.environ['PATH'] = com

os.environ['http_proxy']='http://'+proxy
os.environ['https_proxy']='http://'+proxy
if lis==0:
    com='btfs/bin/btfs daemon'
else:
    com='btfs'+str(lis)+'/bin/btfs daemon'
print(com)
os.system(com)
