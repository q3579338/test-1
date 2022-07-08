'''
Author: honus
Date: 2021-12-17 19:54:38
LastEditTime: 2021-12-17 20:02:07
LastEditors: honus
Description: 
FilePath: \test\get_0_version.py
'''
import xlrd
import xlwt



xls_file=[]

files=os.listdir()
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'xls' in file and 'compare.xls' not in file and 'RECYCLE' not in file:
            xls_file.append(file)

print(xls_file)

for xls in xls_file:
    print(xls)
    data=xlrd.open_workbook("./"+xls,formatting_info=True)
    table=data.sheets()[0]
    version_score=table.col_values(4)[1:]
    if version_score != '0':
