'''
Author: honus
Date: 2022-03-21 20:04:25
LastEditTime: 2022-03-21 20:33:22
LastEditors: honus
Description: 
FilePath: \test\compare_storage_by_floder.py
'''
import xlrd
import xlwt

data = xlrd.open_workbook('./compare_storage.xls',formatting_info=True)
table = data.sheets()[0]
floder = table.col_values(6)[1:]
change = table.col_values(4)[1:]

res = {}

for i in range(len(floder)):
    flo = floder[i].split('\\')[1]
    try:
        res[flo] = [res[flo][0]+change[i],res[flo][1] + 1]
    except:
        res[flo] = [change[i],1]

#print(res)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
flag = 1
tables.write(0, 0, '文件夹')
tables.write(0, 1, '变化量')
for k,v in res.items():
    print(k,v)
    tables.write(flag, 0, k)
    tables.write(flag, 1, v[0]/v[1])
    flag += 1
    excel.save('floder_a.xls')
