import paramiko,json
import re,os
from time import sleep
import xlrd
import xlwt

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet('result')

begin=0
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

    if connect:
        print("%s connect success"%ip)
        tables.write(begin,0,ip)
        tables.write(begin,1,password)
    else:
        print("%s connect fail"%ip+' ,begin next')
        tables.write(begin,2,'connect_failed')
        begin+=1
        continue

    command='cat .streamrDocker/broker-config.json'
    stdin,stdout,stderr=ssh.exec_command(command)
    result=stdout.readlines()
    os.makedirs(ip)
    with open('./'+ip+'/broker-config.json','w') as f:
        f.writelines(result)
    excel.save('get_config_result.xls')
    begin+=1
