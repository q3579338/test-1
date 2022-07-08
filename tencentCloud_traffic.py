'''
Author: honus
Date: 2022-01-17 08:21:26
LastEditTime: 2022-01-17 08:52:15
LastEditors: honus
Description: 
FilePath: /project/tencent.py
'''

import os
import json
import xlwt

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from time import sleep

client_id=''
client_key=''
region='na-siliconvalley'

#23 63
#NAME='ZHUHAI'

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')

tables=excel.get_sheet(0)
tables.write(0, 0, 'ID')
tables.write(0, 1, 'IP')
tables.write(0, 2, 'G_Used')
tables.write(0, 3, 'G_Total')
tables.write(0, 4, 'G_Remain')

Traffic_list=[]

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
    All_Instances={}
    Offset=0
    while Offset < TotalCount:
        instances=common_client.call_json("DescribeInstances",{"Offset":Offset,"Limit":100})["Response"]["InstanceSet"]
        for instance in instances:
            InstanceId=instance["InstanceId"]
            PublicAddresses=instance['PublicAddresses'][0]
            All_Instances[InstanceId]=PublicAddresses
        Offset+=100
        if len(instances)%100!=0 or TotalCount-Offset==0:
            break

    length=len(All_Instances)

    instances_list=[]
    flag=0
    for k,v in All_Instances.items():
        instances_list.append(k)
        if (flag+1)%20==0 or (flag+1)==length:
            #print(len(instances_list))
            TrafficPackages=common_client.call_json('DescribeInstancesTrafficPackages',{"InstanceIds":instances_list})["Response"]["InstanceTrafficPackageSet"]
            for instance in TrafficPackages:
                InstanceId=instance['InstanceId']
                IP=All_Instances[InstanceId]
                Traffic_used=instance['TrafficPackageSet'][0]['TrafficUsed']
                Traffic_total=instance['TrafficPackageSet'][0]['TrafficPackageTotal']
                Traffic_remain=instance['TrafficPackageSet'][0]['TrafficPackageRemaining']
                Traffic_list.append((InstanceId,IP,Traffic_used,Traffic_total,Traffic_remain))
            #print(len(Traffic_list))
            instances_list=[]
        flag+=1

    op=1
    print('共有'+str(len(Traffic_list)))
    for instance in Traffic_list:
        tables.write(op,0,instance[0])
        tables.write(op,1,instance[1])
        tables.write(op,2,int(instance[2])/1024/1024/1024)
        tables.write(op,3,int(instance[3])/1024/1024/1024)
        tables.write(op,4,int(instance[4])/1024/1024/1024)
        op+=1

    excel.save('Traffic_Time.xls')
except TencentCloudSDKException as err:
    print(err)
