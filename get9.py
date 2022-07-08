import xlrd
import os
import xlwt

time='2021_05_08'

files=os.listdir()
xls_files=[]

begin=1
excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'ip')
tables.write(0, 1, 'duokia')
tables.write(0, 2, 'uptime')
tables.write(0, 3, 'Mnemonic')
tables.write(0, 4, 'PeerID')
tables.write(0, 5, 'PrivKey')

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
    uptime_List=table.col_values(11)[1:]
    Mnemonic_list=table.col_values(3)[1:]
    PeerID_list=table.col_values(4)[1:]
    PrivKey_list=table.col_values(5)[1:]
    count=0
    for uptime in uptime_List:
        if uptime!='10':
            tables.write(begin,0,ip_List[count])
            tables.write(begin,1,duokai_List[count])
            tables.write(begin,2,uptime)
            tables.write(begin,3,Mnemonic_list[count])
            tables.write(begin,4,PeerID_list[count])
            tables.write(begin,5,PrivKey_list[count])
            begin+=1
        count+=1
excel.save('result.xls')

