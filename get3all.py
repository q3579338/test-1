'''
Author: honus
Date: 2021-09-09 08:28:38
LastEditTime: 2021-10-03 16:51:37
LastEditors: honus
Description: get 3 with time limit
FilePath: /test/get3all.py
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
tables.write(0,0,'Mnemonic')
tables.write(0,1,'PeerId')
tables.write(0,2,'PrivKey')
tables.write(0,3,'filepath')

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'xls' in file and time in file and '$' not in file:
            xls_files.append(file)

print(xls_files)

begin=1
for xls in xls_files:
    data=xlrd.open_workbook(xls,formatting_info=True)
    table=data.sheets()[0]
    try:
        if table.col_values(3)[0]=='Mnemonic':
            Mnemonic_list=table.col_values(3)[1:]
        elif table.col_values(4)[0]=='Mnemonic':
            Mnemonic_list=table.col_values(4)[1:]
    except:
        print('版本不符合')
    try:
        if table.col_values(4)[0]=='PeerID':
            PeerID_list=table.col_values(4)[1:]
        elif table.col_values(5)[0]=='PeerID':
            PeerID_list=table.col_values(5)[1:]
    except:
        print('版本不符合')
    try:
        if table.col_values(6)[0]=='PrivKey':
            PrivKey_list=table.col_values(6)[1:]
        elif table.col_values(5)[0]=='PrivKey':
            PrivKey_list=table.col_values(5)[1:]
    except:
        print('版本不符合')
        print(xls)


    for key in range(len(PrivKey_list)):
        tables.write(begin,0,Mnemonic_list[key])
        tables.write(begin,1,PeerID_list[key])
        tables.write(begin,2,PrivKey_list[key])
        tables.write(begin,3,xls)
        begin+=1
    del data
    excel.save(time+'.xls')

