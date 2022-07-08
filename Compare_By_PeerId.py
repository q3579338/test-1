'''
Author: honus
Date: 2021-10-03 18:27:46
LastEditTime: 2021-10-03 19:54:32
LastEditors: honus
Description: Compare three config by PeerId
FilePath: /test/Compare_By_PeerId.py
'''
import xlrd
import os
import xlwt

xls_file=[]

files=os.listdir()
for root, dirs, files in os.walk("./", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'xls' in file and 'compare.xls' not in file and 'RECYCLE' not in file:
            xls_file.append(file)
print(xls_file)
all_list=[]
for file in xls_file:
    #print(file)
    data=xlrd.open_workbook("./"+file,formatting_info=True)
    table=data.sheets()[0]
    Mnemonic_List=table.col_values(0)[1:]
    PeerID_List=table.col_values(1)[1:]
    PrivKey_list=table.col_values(2)[1:]
    File_Path=table.col_values(3)[1:]
    for key in range(len(PeerID_List)):
        all_list.append((File_Path[key],Mnemonic_List[key],PeerID_List[key],PrivKey_list[key]))
    del data

count={}
# id (file,Mnemonic,PeerID,PrivKey)
for id in all_list:
    if id[2]=='' or id[2].strip()=='':
        continue
    if count.get(id[2])==None:
        # count {PeerId :(个数 [重复目录,其余两值])}
        count[id[2]]=(0,[])
    tmp_num=count[id[2]][0]+1
    tmp=count[id[2]][1][:]
    tmp.append((id[0],id[1],id[3]))
    count[id[2]]=(tmp_num,tmp)
items=list(count.items())

res_list=[]
# item [PeerId,(count,[file],[Mnemonic],[PrivKey])]
for item in items:
    if item[1][0]>=2:
        id=item[0]
        other=item[1][1]
        res_list.append((id,other))
print('重复个数为:'+str(len(res_list)))

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0,0,'Mnemonic')
tables.write(0,1,'PeerID')
tables.write(0,2,'PrivKey')
tables.write(0,3,'file')

op=1
for res in res_list:
    print(res)
    PeerID=res[0]
    for key in range(len(res[1])):
        file=res[1][key][0]
        Mnemonic=res[1][key][1]
        PrivKey=res[1][key][2]
        tables.write(op,0,Mnemonic)
        tables.write(op,1,PeerID)
        tables.write(op,2,PrivKey)
        tables.write(op,3,file)
        op+=1

# op=1
# for res in res_list:
#     tables.write(op,0,res[0])
#     tables.write(op,1,len(res[1]))
#     flag=2
#     for lis in res[1]:
#         tables.write(op,flag,lis)
#         flag+=1
#     op+=1
excel.save('Compare_PeerId.xls')


