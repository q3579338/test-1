import re,os
from time import sleep
import sys
import paramiko

more=97           #数量-1为实际增加次数，比如要多开64个设置more为65
end=more
max_test=3



res=os.popen('ls').readlines()
maxnumber=0
for data in res:
    geshu=data.find('btfs')
    shu=data.replace('btfs','').replace('\n','')
    if geshu!=-1:
        if shu=='':
            shu=0
        else:
            shu=int(shu)
        if (shu > maxnumber) and shu<=(end-1):
            maxnumber=shu

if maxnumber-1>=more:
    print('exist'+str(maxnumber))
    os._exit(0)

while more-maxnumber>1:
    command='ls -a'
    res=os.popen(command).readlines()
    maxnumber=0
    for data in res:
        geshu=data.find('btfs')
        shu=data.replace('.btfs','').replace('btfs','').replace('\n','')
        if geshu!=-1:
            print(shu)
            if shu=='':
                shu=0
            else:
                shu=int(shu)
            if (shu > maxnumber) and (shu<=(more-1)):
                maxnumber=shu
    print(maxnumber)
    command='cp -r btfs btfs'+str(maxnumber+1)
    print(command)
    os.popen(command)
    sleep(3)
    command='ls -a'
    res=os.popen(command).readlines()
    find=False
    pat='btfs'+str(maxnumber+1)
    print(pat)
    for data in res:
        if data.find(pat)!=-1 and find is False:
            find=True
    if find is False:
        print('copy failed!!!')
    else:
        print('copy success')

    suc=False
    test_test=3
    try:
        username='root'
        port= 22
        ip='127.0.0.1'
        password=''
        client=paramiko.SSHClient()
        key=paramiko.AutoAddPolicy()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, port, username=username, password=password,timeout=30)
    except:
        print('con fail')

    while suc is False and (test_test != 0):
        chan = client.invoke_shell()
        chan.send('cd /root\n')
        sleep(1)
        chan.send('export BTFS_PATH=/root/.btfs'+str(maxnumber+1)+'\n')
        sleep(2)
        chan.send('export PATH=${PATH}:${HOME}/btfs'+str(maxnumber+1)+'/bin\n')
        sleep(2)
        chan.send('btfs init\n')
        sleep(4)

        command='ls -a'
        results = os.popen(command).readlines()

        for data in results:
            pat='.btfs'+str(maxnumber+1)
            #print(pat)
            if data.find(pat)!=-1:
                suc=True
        if suc:
            print("btfs"+str(maxnumber+1)+" init suc")
        elif test_test!=0:
            print("init fail.re")
            test_test=test_test-1
        elif test_test==0:
            print('fail')

    chenggong=False
    test_test=3
    while (chenggong is False) and (test_test!=0):
        chan.send('btfs config profile apply storage-host\n')
        sleep(5)
        print("btfs config profile apply storage-host...")

        command=('ls .btfs'+str(maxnumber+1)+'/ -a')
        test_test-=1
        #print(command)
        results = os.popen(command).readlines()
        for date in results:
            if date.find('config-pre-storage-host')!=-1:
                print('carry apply suc')
                chenggong=True

    command='apt-get -y install screen'
    os.popen(command)
    sleep(2)

    if maxnumber==0:
        command='cat .btfs/config'
    else:
        command='cat .btfs'+str(maxnumber)+'/config'
    print(command)
    res=os.popen(command).readlines()
    duankou=''
    for data in res:
        pat='\"API\": \"/ip4/127.0.0.1/tcp/[0-9]*'
        if re.search(pat,data)!=None:
            duankou=re.search(pat,data).group()
            duankou=duankou[27:len(data)-1]
    print(duankou)
    try:
        newport=int(float(duankou))+1      #5001
    except:
        newport=int(5001+maxnumber+1)
    newadd=newport-5001
    newport1=8080+newadd        #8080
    newport2=6101+newadd        #6101
    newport3=4001+newadd        #4001
    print(newport)
    print(newport1)
    print(newport2)
    print(newport3)
    command='btfs config Addresses.API /ip4/127.0.0.1/tcp/'+str(newport)+'\n'
    print(command)
    chan.send(command)
    sleep(1)
    command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/'+str(newport1)+'\n'
    print(command)
    chan.send(command)
    sleep(1)
    command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/'+str(newport2)+'\n'
    print(command)
    chan.send(command)
    sleep(1)
    command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(newport3)+"\""+",\"/ip6/::/tcp/"+str(newport3)+"\""+"]'"+"\n"
    print(command)
    chan.send(command)
    sleep(1)


    command=('cat .btfs'+str(maxnumber+1)+'/config')
    results = os.popen(command).readlines()
    find=False
    find1=False
    find2=False
    for data in results:
        pat="\"Mnemonic\": (?:'|\").*(?:'|\")"
        if re.search(pat , data)!=None:
            Mnemonic = re.search(pat , data).group()
            Mnemonic = Mnemonic[13:len(Mnemonic)-1]
            print(Mnemonic)
    for data in results:
        pat="\"PeerID\": (?:'|\").*(?:'|\")"
        if re.search(pat , data)!=None:
            PeerID=re.search(pat , data).group()
            PeerID = PeerID[11:len(PeerID)-1]
            print(PeerID)
    for data in results:
        pat="\"PrivKey\": (?:'|\").*(?:'|\")"
        if re.search(pat , data)!=None:
            PrivKey=re.search(pat , data).group()
            PrivKey =PrivKey[12:len(PrivKey)-1]
            print(PrivKey)

    chan.send('screen -S btfs'+str(maxnumber+1)+'\n')
    sleep(3)
    chan.send('export BTFS_PATH=/root/.btfs'+str(maxnumber+1)+'\n')
    sleep(2)
    chan.send('export PATH=${PATH}:${HOME}/btfs'+str(maxnumber+1)+'/bin\n')
    sleep(2)
    chan.send('btfs daemon\n')
    sleep(4)

    print("OK")

    command='ls'
    res=os.popen(command).readlines()
    maxnumber=0
    for data in res:
        geshu=data.find('btfs')
        shu=data.replace('.btfs','').replace('btfs','').replace('\n','')
        if geshu!=-1:
            if shu=='':
                shu=0
            else:
                shu=int(shu)
            if (shu > maxnumber) and (shu<=(more-1)):
                maxnumber=shu
    print(maxnumber)
    command='cp -r btfs btfs'+str(maxnumber+end-1)
    print(command)
    os.popen(command)
    sleep(3)
    command='ls -a'
    res=os.popen(command).readlines()
    find=False
    pat='btfs'+str(maxnumber+end-1)
    print(pat)
    for data in res:
        if data.find(pat)!=-1 and find is False:
            find=True
    if find is False:
        print('copy fail!!!')
    else:
        print('copy suc')

    suc=False
    test_test=3
    while suc is False and (test_test != 0):
        chan = client.invoke_shell()
        chan.send('cd /root\n')
        sleep(1)
        chan.send('export BTFS_PATH=/root/.btfs'+str(maxnumber+end-1)+'\n')
        sleep(2)
        chan.send('export PATH=${PATH}:${HOME}/btfs'+str(maxnumber+end-1)+'/bin\n')
        sleep(2)
        chan.send('btfs init\n')
        sleep(2)

        command='ls -a'
        results = os.popen(command).readlines()
        #print(results)

        for data in results:
            pat='.btfs'+str(maxnumber+end-1)
            #print(pat)
            if data.find(pat)!=-1:
                suc=True
        if suc:
            print("btfs"+str(maxnumber+end-1)+" init suc")
        elif test_test!=0:
            print("init fail,again")
            test_test=test_test-1
        elif test_test==0:
            print('fail')

    chenggong=False
    test_test=3
    while (chenggong is False) and (test_test>0):
        chan.send('btfs config profile apply storage-host\n')
        sleep(5)
        print("carry btfs config profile apply storage-host...")
        command=('ls .btfs'+str(maxnumber+end-1)+'/ -a')
        test_test-=1
        #print(command)
        results = os.popen(command).readlines()
        for date in results:
            if date.find('config-pre-storage-host')!=-1:
                print('carry apply suc')
                chenggong=True

    command='apt-get -y install screen'
    os.popen(command)
    sleep(2)

    command='cat .btfs'+str(maxnumber)+'/config'
    print(command)
    res=os.popen(command).readlines()
    duankou=''
    for data in res:
        pat='\"API\": \"/ip4/127.0.0.1/tcp/[0-9]*'
        if re.search(pat,data)!=None:
            duankou=re.search(pat,data).group()
            duankou=duankou[27:len(data)-1]
    print(duankou)
    try:
        newport=int(float(duankou))+end-1      #5001
    except:
        newport=int(5001+maxnumber+end-1)    #5001
    print('newport is '+str(newport))
    newadd=newport-5001
    newport1=8080+newadd        #8080
    newport2=6101+newadd        #6101
    newport3=4001+newadd        #4001
    print(newport)
    print(newport1)
    print(newport2)
    print(newport3)
    command='btfs config Addresses.API /ip4/127.0.0.1/tcp/'+str(newport)+'\n'
    print(command)
    chan.send(command)
    sleep(1)
    command='btfs config Addresses.Gateway /ip4/127.0.0.1/tcp/'+str(newport1)+'\n'
    print(command)
    chan.send(command)
    sleep(1)
    command='btfs config Addresses.RemoteAPI /ip4/127.0.0.1/tcp/'+str(newport2)+'\n'
    print(command)
    chan.send(command)
    sleep(1)
    command="btfs config --json Addresses.Swarm '[\"/ip4/0.0.0.0/tcp/"+str(newport3)+"\""+",\"/ip6/::/tcp/"+str(newport3)+"\""+"]'"+"\n"
    print(command)
    chan.send(command)
    sleep(1)

    command=('cat .btfs'+str(maxnumber+end-1)+'/config')
    results = os.popen(command).readlines()
    find=False
    find1=False
    find2=False
    for data in results:
        while  data.find("PeerID",0,len(data))!=-1 and find1==False:
            zifu1=data.find("PeerID",0,len(data))
            find1=True
            wri1=data[zifu1+10:len(data)-3]
            print(wri1)
    for data in results:
        while  data.find("PrivKey",0,len(data))!=-1 and find2==False:
            zifu2=data.find("PrivKey",0,len(data))
            find2=True
            wri2=data[zifu2+11:len(data)-2]
            print(wri2)
    for data in results:
        while  data.find("Mnemonic",0,len(data))!=-1 and find==False:
            zifu=data.find("Mnemonic",0,len(data))
            find=True
            wri=data[zifu+12:len(data)-3]
            print(wri)
    s1="sed -i 's/"+wri+"/"+Mnemonic+"/' .btfs"+str(maxnumber+end-1)+"/config"
    print(s1)
    command=(s1)
    os.popen(command)
    s2="sed -i 's/"+wri1+"/"+PeerID+"/' .btfs"+str(maxnumber+end-1)+"/config"
    print(s2)
    command=(s2)
    os.popen(command)
    s3="sed -i 's/"+wri2.replace('/','\/')+"/"+PrivKey.replace('/','\/')+"/' .btfs"+str(maxnumber+end-1)+"/config"
    print(s3)
    command=(s3)
    os.popen(command)

    wri=''
    wri1=''
    wri2=''
    PeerID=''
    Mnemonic=''
    PrivKey=''

    chan.send('screen -S btfs'+str(maxnumber+end-1)+'\n')
    sleep(3)
    chan.send('export BTFS_PATH=/root/.btfs'+str(maxnumber+end-1)+'\n')
    sleep(2)
    chan.send('export PATH=${PATH}:${HOME}/btfs'+str(maxnumber+end-1)+'/bin\n')
    sleep(2)
    chan.send('btfs daemon\n')
    sleep(4)

    print("over")

    #more=more-1
