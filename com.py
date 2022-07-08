import xlrd
import os
import xlwt

data=['2021_05_27','2021_05_28']

xls_files=[]

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, '路径')
tables.write(0, 1, 'ip')
tables.write(0, 2, '1有效节点数')
tables.write(0, 3, '1无效节点数')
tables.write(0, 4, '1平均值')
tables.write(0, 5, '2有效节点数')
tables.write(0, 6, '2无效节点数')
tables.write(0, 7, '2平均值')
tables.write(0, 8, '浮动')

tmp_avg1=0
tmp_avg2=0


for root, dirs, files in os.walk(".", topdown=False):
    xls_file=[]
    for name in files:
        file=os.path.join(root, name)
        if 'xls' in file and file!='storage.xls' and (data[0] in file or data[1] in file):
            xls_file.append(file)
    if xls_file!=[]:
        xls_files.append(xls_file)
print(xls_files)

begin=1
for xls in xls_files:
    if len(xls)!=2:
        tables.write(begin, 0, xls[0])
        tables.write(begin, 1, '该日期有多次数据，请删除后重试！')
        begin+=1
        continue
    else:
        tables.write(begin, 0, xls[0])
        for key in xls:
            if key==xls[0]:
                flag=0
            else:
                flag=1
            data=xlrd.open_workbook(key,formatting_info=True)
            table=data.sheets()[0]
            ip_List=table.col_values(0)[1:]
            storage=table.col_values(8)[1:]
            count=0
            fail_count=0
            all_count=0
            for sto in storage:
                if sto!='':
                    sto=int(sto)
                    all_count+=sto
                    count+=1
                else:
                    fail_count+=1
            if flag==0:
                tmp_avg1=all_count/count
                tables.write(begin, 1, ip_List[0])
                tables.write(begin, 2, count)
                tables.write(begin, 3, fail_count)
                tables.write(begin, 4, tmp_avg1)
                flag=1
            else:
                tmp_avg2=all_count/count
                tables.write(begin, 5, count)
                tables.write(begin, 6, fail_count)
                tables.write(begin, 7, tmp_avg2)
                tables.write(begin, 8, tmp_avg2-tmp_avg1)
            del data
        begin+=1
        excel.save('storage.xls')



