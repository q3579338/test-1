'''
Author: honus
Date: 2022-01-21 18:37:23
LastEditTime: 2022-01-21 18:44:38
LastEditors: honus
Description: 
FilePath: \test\merge_failed_trans.py
'''
import os
import xlrd,xlwt

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'number')
tables.write(0, 2, 'address')
tables.write(0, 3, 'status')

xls_files=[]

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'get_trans_failed' in file and 'xls' in file:
            xls_files.append(file)

print(xls_files)

begin=1

for file in xls_files:
    data=xlrd.open_workbook(file,formatting_info=True)
    table=data.sheets()[0]
    ips=table.col_values(0)[1:]
    numbers=table.col_values(1)[1:]
    addresses=table.col_values(2)[1:]
    status=table.col_values(3)[1:]
    for i in range(len(ips)):
        tables.write(begin, 0, ips[i])
        tables.write(begin, 1, numbers[i])
        tables.write(begin, 2, addresses[i])
        tables.write(begin, 3, status[i])
        begin+=1
    excel.save('all_failed_address.xls')
