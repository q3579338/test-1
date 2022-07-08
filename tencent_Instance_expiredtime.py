import os
import json
import xlwt

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
import time

client_id=''
client_key=''
region='na-siliconvalley'

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'Id')
tables.write(0, 1, 'Name')
tables.write(0, 2, 'Ip')
tables.write(0, 3, 'Time')
flag = 1
#now_time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()) 

try:
    cred = credential.Credential(client_id,client_key)
    httpProfile = HttpProfile()
    # 域名首段必须和下文中CommonClient初始化的产品名严格匹配
    httpProfile.endpoint = "lighthouse.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile

    # 实例化要请求的common client对象，clientProfile是可选的。
    common_client = CommonClient("lighthoue",version='2020-03-24' ,credential=cred, region=region, profile=clientProfile)
    # 接口参数作为json字典传入，得到的输出也是json字典，请求失败将抛出异常
    instances=common_client.call_json("DescribeInstances", {"Limit": 1})['Response']
    #print(instances)
    TotalCount=instances['TotalCount']
    All_Instances=[]
    Offset=0
    while Offset < TotalCount:
        instances=common_client.call_json("DescribeInstances",{"Offset":Offset,"Limit":100})["Response"]["InstanceSet"]
        for instance in instances:
            InstanceId=instance["InstanceId"]
            InstanceName=instance['InstanceName']
            PublicAddresses=instance['PublicAddresses'][0]
            ExpiredTime=instance['ExpiredTime']
            All_Instances.append((InstanceId,InstanceName,PublicAddresses,ExpiredTime))
        Offset+=100
        if len(instances)%100!=0 or TotalCount-Offset==0:
            break
    
    print(len(All_Instances))
    for instance in All_Instances:
        tables.write(flag,0,instance[0])
        tables.write(flag,1,instance[1])
        tables.write(flag,2,instance[2])
        tables.write(flag,3,instance[3])
        flag+=1
        excel.save('Time.xls')
    
except TencentCloudSDKException as err:
    print(err)
