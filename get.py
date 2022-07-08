import os
import xlrd
import xlwt
from time import strftime, localtime
from datetime import timedelta, datetime

yesterday = (datetime.today() + timedelta(-1)).strftime('%Y_%m_%d')
today=strftime('%Y_%m_%d',localtime())
print(today)
print(yesterday)
pipei=0
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0,'今日BTFS数量')
tables.write(0, 1,'今日合约数')
tables.write(0, 2,'今日平均值')

tables.write(0, 4,'昨日BTFS数量')
tables.write(0, 5,'昨日合约数')
tables.write(0, 6,'昨日平均值')

tables.write(0,8,'总变化量')
tables.write(0,9,'平均变化率')

tables.write(0,11,'ip')
tables.write(0,12,'今日文件路径')
tables.write(0,13,'昨日文件路径')
tables.write(0,14,'今日获取失败节点数')
tables.write(0,15,'昨日获取失败节点数')

today_files=[]
files=os.listdir()
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if today in file and 'RECYCLE' not in file:
            today_files.append(file)

yesterday_files=[]
files=os.listdir()
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if yesterday in file and 'RECYCLE' not in file:
            yesterday_files.append(file)

today_detail={}
for xls in today_files:
    print(xls)
    data=xlrd.open_workbook(xls,formatting_info=True)
    table=data.sheets()[0]
    ip=table.col_values(0)[1]
    today_detail[ip]=xls
    del data

yesterday_datail={}
for xls in yesterday_files:
    print(xls)
    data=xlrd.open_workbook(xls,formatting_info=True)
    table=data.sheets()[0]
    ip=table.col_values(0)[1]
    yesterday_datail[ip]=xls
    del data

del today_files
del yesterday_files

print(today_detail)
print(yesterday_datail)
print('今日表格数量: '+str(len(today_detail)))
print('昨日表格数量: '+str(len(yesterday_datail.items())))

flag=1
queshi_list=[]
for k,v in today_detail.items():
    if k in yesterday_datail:
        pipei+=1
        file1=v
        file2=yesterday_datail[k]
        data1=xlrd.open_workbook(file1,formatting_info=True)
        data2=xlrd.open_workbook(file2,formatting_info=True)
        table1=data1.sheets()[0]
        table2=data2.sheets()[0]
        ip1_List=table1.col_values(0)[1:]
        ip2_List=table2.col_values(0)[1:]
        ip1=ip1_List[0]
        ip2=ip2_List[0]
        duokai1_List=table1.col_values(2)[1:]
        duokai2_List=table2.col_values(2)[1:]
        duokai1_count=len(duokai1_List)
        duokai2_count=len(duokai2_List)
        active1_List=table1.col_values(9)[1:]
        active2_List=table2.col_values(9)[1:]
        active1_count=0
        active2_count=0
        fail1=0
        fail_List=table1.col_values(11)[1:]
        for fail in fail_List:
            if isinstance(fail,str) and fail!='':
                fail1=fail1+1
        print(fail1)
        fail2=0
        fail_List=table2.col_values(11)[1:]
        for fail in fail_List:
            if isinstance(fail,str) and fail!='':
                fail2=fail2+1
        print(fail2)

        try:
            key_List=[]
            for key in range(len(active1_List)):
                if active1_List[key]=='' or active2_List[key]=='':
                    key_List.append(key)
        except:
            pass

        value=0
        key_List=sorted(set(key_List),key=key_List.index)
        for key in key_List:
            print('key:'+str(key))
            del active1_List[key-value]
            del active2_List[key-value]
            value+=1
        for active in active1_List:
            try:
                active=int(active)
                active1_count+=active
            except:
                continue
        for active in active2_List:
            try:
                active=int(active)
                active2_count+=active
            except:
                continue
        print(duokai1_count)
        print(active1_count)
        print(duokai2_count)
        print(active2_count)
        tables.write(flag, 0, duokai1_count)
        tables.write(flag, 1, active1_count)
        tables.write(flag, 2, active1_count/duokai1_count)
        tables.write(flag, 4, duokai2_count)
        tables.write(flag, 5, active2_count)
        tables.write(flag, 6, active2_count/duokai2_count)
        tables.write(flag, 8, active1_count-active2_count)
        tables.write(flag, 9, (active1_count-active2_count)/duokai1_count)
        tables.write(flag, 11, ip1)
        tables.write(flag, 12, file1)
        tables.write(flag, 13, file2)
        tables.write(flag, 14, fail1)
        tables.write(flag, 15, fail2)
        flag+=1

        del yesterday_datail[k]

        excel.save('com.xls')
    else:
        queshi_list.append(k)

print('匹配成功:'+str(pipei)+'个')
