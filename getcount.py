import xlrd
import xlwt
import os

key='2021_08_03'
all_files=[]

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('data')
tables=excel.get_sheet('data')
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if key in file:
            all_files.append(file)

print(all_files)
count=0
for file in all_files:
    print(file)
    data=xlrd.open_workbook(file,formatting_info=True)
    table=data.sheets()[0]
    ip_List=table.col_values(0)                 #List
    yue_List=table.col_values(7)
    try:
        screen_List=table.col_values(17)
        screen_count=screen_List[1]
    except:
        screen_count=''
    ip=ip_List[1]
    del ip_List
    print(ip)
    yue_count=0
    for yue in yue_List[1:]:
        try:
            yue_count+=int(yue)
        except:
            continue
    print(yue_count)
    tables.write(count,0,ip)
    tables.write(count,1,file)
    tables.write(count,2,yue_count)
    tables.write(count,3,screen_count)
    count+=1
    excel.save('yue_count.xls')