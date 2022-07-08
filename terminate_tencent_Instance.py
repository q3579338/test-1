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
region='na-siliconvalley'

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
            PublicAddresses=instance['PublicAddresses'][0]
            ExpiredTime=instance['ExpiredTime']
            if ExpiredTime <= now_time:
                All_Instances.append((InstanceId,InstanceName,PublicAddresses,ExpiredTime))
        Offset+=100
        if len(instances)%100!=0 or TotalCount-Offset==0:
            break
    
    print(len(All_Instances))
    op=[]
    while len(All_Instances)>0:
        op.append(All_Instances.pop()[0])
        if len(op)==100:
            common_client.call_json("TerminateInstances",{"InstanceIds":op})
            op=[]
    TerminateInstances=common_client.call_json('TerminateInstances',{"InstanceIds": op})['Response']
    print(TerminateInstances)
except TencentCloudSDKException as err:
    print(err)
