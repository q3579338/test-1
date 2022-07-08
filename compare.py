import xlrd
import os
import xlwt

xls_file=[]

files=os.listdir()
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'xls' in file and 'compare.xls' not in file and 'RECYCLE' not in file:
            xls_file.append(file)

all_list=[]
for file in xls_file:
    #print(file)
    data=xlrd.open_workbook("./"+file,formatting_info=True)
    table=data.sheets()[0]
    PeerID_List=table.col_values(4)[1:]
    for peerid in PeerID_List:
        all_list.append((file,peerid))
    del data

count={}
for id in all_list:
    if id[1]=='' or id[1].strip()=='':
        continue
    if count.get(id[1])==None:
        count[id[1]]=(0,[])
    tmp_num=count[id[1]][0]+1
    tmp=count[id[1]][1][:]
    tmp.append(id[0])
    count[id[1]]=(tmp_num,tmp)
items=list(count.items())
res_list=[]
for item in items:
    if item[1][0]>=2:
        id=item[0]
        table=item[1][1]
        table.sort()
        res_list.append((id,table))
print('重复个数为:'+str(len(res_list)))

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'PeerID')
tables.write(0, 1, 'file')

op=1

for res in res_list:
    tables.write(op,0,res[0])
    tables.write(op,1,len(res[1]))
    flag=2
    for lis in res[1]:
        tables.write(op,flag,lis)
        flag+=1
    op+=1
excel.save('compare.xls')