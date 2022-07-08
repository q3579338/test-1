import requests
import re
import xlwt
import xlrd
from time import sleep
data=xlrd.open_workbook("./failed.xls",formatting_info=True)
table=data.sheets()[0]
name_List=table.col_values(0)

data1=xlrd.open_workbook("./data.xls",formatting_info=True)
table1=data1.sheets()[0]
xuhao_List=table1.col_values(0)
ip_List=table1.col_values(1)
# group_List=table.col_values(3)

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('ip')
tables=excel.get_sheet('ip')

row=table.nrows

i=0
a=[]
begin=0
while i<row:
    name=name_List[i]
    if 'SEA' in name:
        i+=1
        continue              #44
    xuhao=xuhao_List.index(name)
    ip=ip_List[xuhao]
    tables.write(begin,0,ip)
    tables.write(begin,1,'')
    tables.write(begin,2,name)
    begin+=1
    print(xuhao)
    i+=1
print(len(a))
excel.save('all1.xls')



def getlist():
    url='http://209.126.9.94/server'
    cookies={"nezha-dashboard":"149e68864049645374530c604e38184d"}
    res=requests.get(url=url,cookies=cookies).text

    pat='<tr>[\s\S]*?</tr>'
    begin=re.findall(pat,res)
    pat='<td>[\s\S]*?</td>'
    a=[]
    k=0
    for i in begin[1:]:
        end=re.findall(pat,i)
        if end[3]=='<td></td>':
            #删除
            all=end[0].replace('<td>','').replace('</td>','').replace('(0)','')
            print(all)
            delwy(all)
            #记录
            # all1=end[1].replace('<td>','').replace('</td>','')
            # tables.write(k,0,all1)
            # k+=1
    print(len(a))
    #

def delwy(i):
    cookies={"nezha-dashboard":"149e68864049645374530c604e38184d"}
    url='http://209.126.9.94/api/server/'+str(i)
    res=requests.delete(url=url,cookies=cookies)
    print(res.text)
