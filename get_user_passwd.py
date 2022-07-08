import requests
import os,xlwt,json

excel = xlwt.Workbook()
sheet = excel.add_sheet('data')
sheet.write(0,0,'路径')
sheet.write(0,1,'密码')
sheet.write(0,2,'地址')
sheet.write(0,3,'余额')

files_list=[]
for root,dirs,files in os.walk('.',topdown=False):
    if ('password' or 'UTC') in files:
        files_list.append([root,files])

flag=1
for file in files_list:
    key=file[0]
    values=file[1]
    for value in values:
        if 'password' in value:
            path=key+'\\'+value
            with open(path,'r') as f:
                data=f.readline()
                print('path: '+key+'\\'+value)
                print('passwrod: '+ data)
                sheet.write(flag,0,key)
                sheet.write(flag,1,data)
        if 'UTC' in value:
            path=key+'\\'+value
            with open(path,'r') as f:
                data=f.readline()
                data=json.loads(data)['address']
                print('address: '+data)
                sheet.write(flag,2,data)
            url='https://airdrop-cache.ethswarm.org/balances/0x'+data
            headers={
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
                'origin': 'https://airdrop.ethswarm.org',
                'referer': 'https://airdrop.ethswarm.org/',
                'sec-fetch-dest': 'empty',
                'sec-fetch-site': 'same-site',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
            }
            res=requests.get(url=url,headers=headers)
            print('res.text: '+res.text)
            if res.text=='' or res.text=='{}':
                continue
            res=json.loads(res.text)
            balance=format(int(res['balance'])/10000000000000000,'.6f')
            sheet.write(flag,3,balance)
    flag+=1
    excel.save('key_passwd.xls')
