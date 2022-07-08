import xlrd
import os
import xlwt
import openpyxl

time='all_privKey'

files=os.listdir()
xls_files=[]

all_key=[]
begin=1
excel=openpyxl.Workbook()
sheet = excel.get_sheet_by_name('Sheet') 

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'xls' in file and 'all_privKey' not in file and '$' not in file:
            xls_files.append(file)

print(xls_files)

begin=1
for xls in xls_files:
    data=xlrd.open_workbook(xls,formatting_info=True)
    table=data.sheets()[0]
    try:
        if table.col_values(6)[0]=='PrivKey':
            PrivKey_list=table.col_values(6)[1:]
        elif table.col_values(5)[0]=='PrivKey':
            PrivKey_list=table.col_values(5)[1:]
        elif table.col_values(4)[0]=='PrivKey':
            PrivKey_list=table.col_values(4)[1:]
    except:
        continue

    print('xls name is :'+xls)
    for key in range(len(PrivKey_list)):
        if PrivKey_list[key] not in all_key:
            sheet.cell(row=begin,column=1,value=PrivKey_list[key])
            begin+=1
            all_key.append(PrivKey_list[key])
    del data
    excel.save(time+'.xlsx')

