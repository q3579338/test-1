import os
import xlrd
import xlwt
from time import strftime, localtime
from datetime import timedelta, datetime

yesterday = (datetime.today() + timedelta(-1)).strftime('%Y_%m_%d')
today=strftime('%Y_%m_%d',localtime())
print(today)
print(yesterday)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, '今日硬盘总量')
tables.write(0,1,'昨日硬盘总量')
tables.write(0,2,'单日总节点数')
tables.write(0,3,'总变化量')
tables.write(0,4,'平均变化率')

tables.write(0,5,'ip')
tables.write(0,6,'今日文件路径')
tables.write(0,7,'昨日文件路径')
tables.write(0,8,'今日获取失败节点数')
tables.write(0,9,'昨日获取失败节点数')

#获取符合日期要求的xls文件
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

#获取xls对应ip
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
print('昨日表格数量: '+str(len(yesterday_datail)))

#遍历上述列表，根据ip为标准获取对应xls，若匹配，则开始对比，否则计入失败列表。
flag=1
queshi_list=[]
for k,v in today_detail.items():
    if k in yesterday_datail:
        file1=v
        file2=yesterday_datail[k]
        data1=xlrd.open_workbook(file1,formatting_info=True)
        data2=xlrd.open_workbook(file2,formatting_info=True)
        table1=data1.sheets()[0]
        table2=data2.sheets()[0]
        duokai1_List=table1.col_values(2)[1:]
        duokai2_List=table2.col_values(2)[1:]
        duokai1_count=len(duokai1_List)
        duokai2_count=len(duokai2_List)
        storage1_List=table1.col_values(8)[1:]
        storage2_List=table2.col_values(8)[1:]
        count1=0
        count2=0
        all_count=0
        yesterday_fail=0
        today_fail=0
        for key in range(0,len(storage1_List)):
            try:
                sto1=float(storage1_List[key])
            except:
                yesterday_fail+=1
                continue
            try:
                sto2=float(storage2_List[key])
            except:
                today_fail+=1
                continue
            count1+=sto1
            count2+=sto2
            all_count+=1
        print(count1)
        print(count2)
        tables.write(flag,0,count1)
        tables.write(flag,1,count2)
        tables.write(flag,2,all_count)
        tables.write(flag,3,count1-count2)
        try:
            tables.write(flag,4,(count1-count2)/all_count)
        except:
            tables.write(flag,4,0)
        tables.write(flag,5,k)
        tables.write(flag,6,file1)
        tables.write(flag,7,file2)
        tables.write(flag,8,yesterday_fail)
        tables.write(flag, 9,today_fail)
        flag+=1

        del yesterday_datail[k]

        excel.save('compare_storage.xls')
    else:
        queshi_list.append(k)
