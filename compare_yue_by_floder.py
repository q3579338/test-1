'''
Author: honus
Date: 2022-03-22 18:26:47
LastEditTime: 2022-03-22 18:29:35
LastEditors: honus
Description: 
FilePath: \test\compare_yue_by_floder.py
'''
import xlrd
import xlwt

data = xlrd.open_workbook('./余额统计.xls',formatting_info=True)
table = data.sheets()[0]
floder = table.col_values(1)
yue = table.col_values(2)
res = {}
for i in range(len(floder)):
    flo = floder[i].split('\\')[1]
    try:
        res[flo] = [res[flo][0]+yue[i],res[flo][1] + 1]
    except:
        res[flo] = [yue[i],1]

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
flag = 1
tables.write(0, 0, '文件夹')
tables.write(0, 1, '变化量')

for k , v in res.items():
    print(k,v)
    tables.write(flag, 0, k)
    tables.write(flag, 1, v[0]/v[1])
    flag += 1
    excel.save('floder_b.xls')
