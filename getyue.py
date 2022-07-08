import xlrd
import os
import xlwt

time='2021_06_21'

files=os.listdir()
xls_files=[]

begin=1
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'duokia')
tables.write(0, 2, 'yue')
tables.write(0, 3, 'Key')

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if time in file:
            xls_files.append(file)


for xls in xls_files:
    data=xlrd.open_workbook(xls,formatting_info=True)
    table=data.sheets()[0]
    ip_List=table.col_values(0)[1:]
    duokai_List=table.col_values(2)[1:]
    yue_List=table.col_values(7)[1:]
    key_List=table.col_values(5)[1:]
    count=0
    for yue in yue_List:
        if yue!='0':
            tables.write(begin,0,ip_List[count])
            tables.write(begin,1,duokai_List[count])
            tables.write(begin,2,yue)
            tables.write(begin,3,key_List[count])
            begin+=1
            try:
                print(ip_List[count],'  ',int(duokai_List[count]),'  ',yue)
            except:
                print(ip_List[count],'  ',duokai_List[count],'  ',yue)
        count+=1
excel.save('yue.xls')

