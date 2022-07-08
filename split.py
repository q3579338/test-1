import xlrd
import xlwt
import os

data=xlrd.open_workbook("./data.xls",formatting_info=True)
table=data.sheets()[0]
ip_List=table.col_values(0)
password_List=table.col_values(1)
first_List=table.col_values(2)
second_List=table.col_values(3)
third_List=table.col_values(4)
row=table.nrows

max=3

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def copy(count):
    command='copy getbalance120.py .\\'+str(count)+'\\getbalance120.py'
    print(command)
    os.system(command)

count=0
flag=0
n=0
while count<row:
    ip=ip_List[count]
    password=password_List[count]
    mkdir(str(count+1))
    copy(count+1)
    excel = xlwt.Workbook(encoding = 'utf-8')
    tables = excel.add_sheet('ip')
    tables=excel.get_sheet(0)
    tables.write(0, 0, ip)
    tables.write(0, 1, password)
    while (flag>=count*max and flag<(count+1)*max):
        try:
            first=first_List[flag]
            second=second_List[flag]
            third=third_List[flag]
        except:
            first=''
            second=''
            third=''
        tables.write(flag-count*max, 2, first)
        tables.write(flag-count*max, 3, second)
        tables.write(flag-count*max, 4, third)
        flag=flag+1
    excel.save('./'+str(count+1)+'/data.xls')
    count+=1
