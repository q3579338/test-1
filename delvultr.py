import requests
import json
from time import sleep

API='RRXWVNXKTA2SU26JRTG6XSJHKSPLEMMNPQ7A'
ip_List=['155.138.222.50','149.28.119.82','144.202.50.135','216.128.130.64','45.32.5.170']

instances_url='https://api.vultr.com/v2/instances'

headers={
    'Authorization': 'Bearer '+str(API)
}
res=requests.get(instances_url,headers=headers)
all_instances=json.loads(res.text)
for instances in all_instances['instances']:
    ip=instances['main_ip']
    id=instances['id']
    if ip not in ip_List:
        delete_url='https://api.vultr.com/v2/instances/'
        delete_url=delete_url+id
        res=requests.delete(url=delete_url,headers=headers)
        if str(res.status_code)!='204':
            print(ip+' 删除失败')
        print(ip+' 删除成功')
        sleep(4)
    else:
        print(ip)


