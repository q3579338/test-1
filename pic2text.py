'''
Author: honus
Date: 2022-01-07 23:20:55
LastEditTime: 2022-01-07 23:47:53
LastEditors: honus
Description: 
FilePath: \Code\pic2text.py
'''
import requests 
import urllib
import base64
import json
import os
import xlwt
import time

client_id=''
client_secret=''

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet('result')
tables.write(0, 0, '文件名')
tables.write(0, 1, '姓名')
tables.write(0, 2, '临床诊断')

files=os.listdir('./')
files=[ i for i in files if i.endswith('.jpg')]

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
response = requests.get(host)
if response:
    access_token=response.json()['access_token']

flag=1
for file in files:

    url='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    headers={
        'Content-Type':'application/x-www-form-urlencoded'
    }

    with open(file,'rb') as f:
        base_img=base64.b64encode(f.read())

    data={
        'access_token': access_token,
        'image': base_img
    }

    res=requests.post(url,data=data,headers=headers)
    #print(res.text)
    if res:
        res=json.loads(res.text)['words_result']
        for i in res:
            if '姓名' in i['words']:
                name=i['words']
            if '临床诊断' in i['words']:
                cases=i['words']

    print(file.replace('.jpg',''),name.replace('姓名:',''),cases.replace('临床诊断:',''))
    tables.write(flag, 0, file.replace('.jpg',''))
    tables.write(flag, 1, name.replace('姓名:',''))
    tables.write(flag, 2, cases.replace('临床诊断:',''))
    flag+=1
    excel.save('result.xls')
    time.sleep(1)