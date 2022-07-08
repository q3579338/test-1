'''
Author: honus
Date: 2022-03-16 19:24:48
LastEditTime: 2022-03-16 21:07:48
LastEditors: honus
Description: 
FilePath: \test\SplitByNum.py
'''
import xlrd
import xlwt
import os

Num = 8

data = xlrd.open_workbook('data.xls')

table = data.sheets()[0]
OldIps = table.col_values(0)[1:]
OldPasswords = table.col_values(1)[1:]
NewIps = table.col_values(2)[1:]
NewPasswords = table.col_values(3)[1:]

OldIps = [i for i in OldIps if i != '']
NewIps = [i for i in NewIps if i != '']

flag = 1
index = 0
for i in range(len(OldIps)):
    excel = xlwt.Workbook(encoding='utf-8')
    tables = excel.add_sheet('result')
    tables.write(0, 0, 'OldIp')
    tables.write(0, 1, 'OldPassword')
    tables.write(0, 2, 'NewIp')
    tables.write(0, 3, 'NewPassword')

    tables.write(1, 0, OldIps[i])
    tables.write(1, 1, OldPasswords[i])
    
    k = 1
    while k <= Num and index < len(NewIps):
        tables.write( k , 2, NewIps[index])
        tables.write( k , 3, NewPasswords[index])
        k += 1
        index += 1

    if not os.path.exists('./'+str(flag)):
        os.mkdir('./' + str(flag))
    excel.save('./'+ str(flag)  + '/data.xls')
    flag += 1
