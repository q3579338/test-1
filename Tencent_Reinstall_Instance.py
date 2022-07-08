'''
Author: honus
Date: 2022-03-17 22:20:14
LastEditTime: 2022-03-19 15:39:39
LastEditors: honus
Description: 
FilePath: \test\Tencent_Reinstall_Instance.py
'''
import os
import json

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
import time

client_id=''
client_key=''
region='eu-frankfurt'
name='6dph'
ImageId = ''
now_time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime()) 

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
            All_Instances.append((InstanceId,InstanceName))
        Offset+=100
        if len(instances)%100!=0 or TotalCount-Offset==0:
            break

    All_Instances = [i for i in All_Instances if name in i[1]]

    print(len(All_Instances))

    for instance in All_Instances:
        instance=instance[0]
        try:
            res = common_client.call_json("ResetInstance",{"InstanceId":instance,"BlueprintId": ImageId})
            print(res)
            print(instance)
            time.sleep(1)
        except TencentCloudSDKException as err:
            print(err)

except TencentCloudSDKException as err:
    print(err)
