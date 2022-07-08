import os
import json

from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from time import sleep

client_id=''
client_key=''
region='ap-hongkong'
name=''
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
            #print(instance)
            InstanceId=instance["InstanceId"]
            InstanceName=instance['InstanceName']
            PublicAddresses=instance['PublicAddresses'][0]
            All_Instances.append((InstanceId,InstanceName,PublicAddresses))
        Offset+=100
        if len(instances)%100!=0 or TotalCount-Offset==0:
            break
    
    All_Instances=[k for k in All_Instances if name in k[1]]
    #print(All_Instances)
    #sleep(99)
    return_list=[]
    for instance in All_Instances:
        InstanceId=instance[0]
        print(InstanceId+" "+instance[1]+" "+instance[2])
        FireWall=common_client.call_json('DescribeFirewallRules',{"InstanceId":InstanceId,"Limit":100})['Response']
        flag=False
        for rule in FireWall['FirewallRuleSet']:
            if rule['Protocol']=='ALL' and rule['Port']=='ALL':
                print('已放行')
                flag=True
                break
        if not flag:
            return_list.append((InstanceId,' ',instance[1],' ',instance[2]))
            print('未放行')
            #Add_FireWall=common_client.call_json('CreateFirewallRules',{"InstanceId":InstanceId,"FirewallRules":[{"Protocol":"ALL","Port":"ALL","CidrBlock":"0.0.0.0/0","Action":"ACCEPT"}]})
    print("共有实例"+str(len(All_Instances))+"台")
    print("未放行实例"+str(len(return_list))+"台")
    for k in return_list:
        print(k)
except TencentCloudSDKException as err:
    print(err)