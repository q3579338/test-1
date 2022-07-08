'''
Author: honus
Date: 2021-09-09 08:28:38
LastEditTime: 2022-02-11 17:33:35
LastEditors: honus
Description: get 3 with time limit
FilePath: \test\get_address.py
'''
import xlrd
import os
import xlwt

time='10_03'

files=os.listdir()
xls_files=[]

all_key=[]
begin=1
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)

tables.write(0,2,'address')



for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'xls' in file and '$' not in file and 'result' in file:
            xls_files.append(file)

print(xls_files)

begin=1
for xls in xls_files:
    data=xlrd.open_workbook(xls,formatting_info=True)
    table=data.sheets()[0]
    address=table.col_values(3)[1:]
    if '0x' not in address[0]:
        continue
    for i in range(len(address)):
        tables.write(begin,2,address[i])
        begin+=1
    excel.save('address.xls')

