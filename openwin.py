import os
import subprocess
import xlrd


data=xlrd.open_workbook("./1.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)                 #List
password_List=table.col_values(1)           #List
#行数
row=table.nrows
i=0
while i<row:
    ip=ip_List[i]
    password=password_List[i]
    print(ip)
    print(password)
    command='PowerShell -Command \"(\\"'+password+'\\" | ConvertTo-SecureString -AsPlainText -Force) | ConvertFrom-SecureString;\"'
    res=os.popen(command).readlines()
    encodepassword=res[0].replace('\n','')
    content='''screen mode id:i:1
desktopwidth:i:1280
desktopheight:i:750
session bpp:i:24
winposstr:s:2,3,188,8,1062,721
full address:s:'''+str(ip)+'''
compression:i:1
keyboardhook:i:2
audiomode:i:0
redirectdrives:i:0
redirectprinters:i:0
redirectcomports:i:0
redirectsmartcards:i:0
displayconnectionbar:i:1
autoreconnection
enabled:i:1
username:s:administrator
domain:s:MicrosoftAccount
alternate shell:s:
shell working directory:s:
password 51:b:'''+str(encodepassword)+'''
disable wallpaper:i:1
disable full window drag:i:1
disable menu anims:i:1
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1'''
    with open(ip+'.rdp','w+') as f:
        f.write(content)
    # command='MSTSC '+str(i+1)+'.rdp'
    # os.system(command)
    i=i+1

