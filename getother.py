# -*- coding: utf-8 -*-
import requests
import json
import xlwt
from time import sleep
import time

now_time=time.strftime("%Y-%m-%d", time.localtime()) 
def getnext(addr):
    url='https://apiasia.tronscan.io:5566/api/transfer?sort=-timestamp&count=true&limit=2&start=0&address='+addr+'&direction=out'
    res=requests.get(url=url)
    res=json.loads(res.text)
    if res['data']==[]:
        return False
    elif res['data'][0]['transferFromAddress']==addr:
        return res['data'][0]['transferToAddress']
    else:
        return False

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('result')
tables=excel.get_sheet(0)
tables.write(0, 0, 'host_id')
tables.write(0, 1, 'addrA')
tables.write(0, 2, 'addrB')
tables.write(0, 3, 'addrC')
tables.write(0, 4, 'addrD')
tables.write(0, 5, 'location')

begin=1
url1='https://data.btfs.io/api/btfsscan/rank'
headers1={
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7',
    'content-length': '56',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://scan.bt.io',
    'referer': 'https://scan.bt.io/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
}
data={"rank_flag":2,"is_suspect":False,"limit":200,"start":0}
res=requests.post(url=url1,headers=headers1,data=json.dumps(data))
if res.status_code==200:
    all_data=json.loads(res.text)['data']
    all_id=[]
    for data in all_data:
        id=data['host_pid']
        all_id.append(id)
    for id in all_id:
        url2='https://data.btfs.io/api/btfsscan/check_node_id?node_id='+id
        headers2={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'
        }
        res=requests.get(url=url2,headers=headers2)
        res=json.loads(res.text)['data']
        if res==True:
            url3='https://data.btfs.io/api/btfsscan/search/node_info?node_id='+id
            res=requests.get(url=url3,headers=headers2)
            if res.status_code==200:
                res=json.loads(res.text)['data']
                tron_wallet_addr=res['tron_wallet_addr']
                flag=2
                next=tron_wallet_addr
                while flag<5:
                    sleep(3)
                    next=getnext(next)
                    if not next:
                        break
                    tables.write(begin, flag, next)
                    flag+=1
                location=res['country']
                cou=[["af", "阿富汗"],["hk",'香港'],["cn","中国"],["al", "阿尔巴尼亚"], ["dz", "阿尔及利亚"], ["us", "美国"], ["ad", "安道尔"], ["ao", "安哥拉"], ["ag", "安提瓜和巴布达"], ["ae", "阿联酋"], ["ar", "阿根廷"], ["am", "亚美尼亚"], ["au", "澳大利亚"], ["at", "奥地利"], ["az", "阿塞拜疆"], ["bs", "巴哈马"], ["bh", "巴林"], ["bd", "孟加拉"], ["bb", "巴巴多斯"], ["by", "白俄罗斯"], ["be", "比利时"], ["bz", "伯利兹"], ["bj", "贝宁"], ["bt", "不丹"], ["bo", "玻利维亚"], ["ba", "波斯尼亚"], ["bw", "博茨瓦纳"], ["br", "巴西"], ["bn", "文莱"], ["bg", "保加利亚"], ["bf", "布基纳法索"], ["bi", "布隆迪"], ["kh", "柬埔寨"], ["cm", "喀麦隆"], ["ca", "加拿大"], ["cf", "中非"], ["td", "乍得"], ["cl", "智利"], ["co", "哥伦比亚"], ["km", "科摩罗"], ["cd", "刚果布"], ["cg", "刚果金"], ["cr", "哥斯达黎加"], ["ci", "科特迪瓦"], ["hr", "克罗地亚"], ["cy", "塞浦路斯"], ["cz", "捷克"], ["dk", "丹麦"], ["dj", "吉布提"], ["dm", "多米尼克"], ["do", "多米尼加"], ["ec", "厄瓜多尔"], ["eg", "埃及"], ["sv", "萨尔瓦多"], ["gb", "英国"], ["gq", "赤道几内亚"], ["er", "厄立特里亚"], ["ee", "爱沙尼亚"], ["et", "埃塞俄比亚"], ["fj", "斐济"], ["fi", "芬兰"], ["fr", "法国"], ["ga", "加蓬"], ["gm", "冈比亚"], ["ge", "格鲁吉亚"], ["de", "德国"], ["gh", "加纳"], ["gr", "希腊"], ["gd", "格林纳达"], ["gt", "危地马拉"], ["cu", "古巴"], ["gn", "几内亚"], ["gw", "几内亚比绍"], ["gy", "圭亚那"], ["ht", "海地"], ["nl", "荷兰"], ["hn", "洪都拉斯"], ["hu", "匈牙利"], ["is", "冰岛"], ["in", "印度"], ["id", "印尼"], ["ir", "伊朗"], ["iq", "伊拉克"], ["ie", "爱尔兰"], ["il", "以色列"], ["it", "意大利"], ["jm", "牙买加"], ["jp", "日本"], ["jo", "约旦"], ["kz", "哈萨克斯坦"], ["ke", "肯尼亚"], ["kg", "吉尔吉斯"], ["ki", "基里巴斯"], ["kr", "韩国"], ["kw", "科威特"], ["la", "老挝"], ["lv", "拉脱维亚"], ["lb", "黎巴嫩"], ["ls", "莱索托"], ["lr", "利比里亚"], ["ly", "利比亚"], ["li", "列支敦士登"], ["lt", "立陶宛"], ["lu", "卢森堡"], ["mk", "马其顿"], ["mg", "马达加斯加"], ["mw", "马拉维"], ["my", "马来西亚"], ["mv", "马尔代夫"], ["ml", "马里"], ["mt", "马耳他"], ["mh", "马绍尔群岛"], ["mr", "毛里塔尼亚"], ["mu", "毛里求斯"], ["mx", "墨西哥"], ["fm", "密克罗尼西亚"], ["md", "摩尔多瓦"], ["mc", "摩纳哥"], ["mn", "蒙古"], ["me", "黑山共和国"], ["ma", "摩洛哥"], ["mz", "莫桑比克"], ["mm", "缅甸"], ["na", "纳米比亚"], ["nr", "瑙鲁"], ["np", "尼泊尔"], ["nz", "新西兰"], ["ni", "尼加拉瓜"], ["ne", "尼日尔"], ["ng", "尼日利亚"], ["kp", "朝鲜"], ["no", "挪威"], ["om", "阿曼"], ["pk", "巴基斯坦"], ["pw", "帕劳"], ["ps", "巴勒斯坦"], ["pa", "巴拿马"], ["pg", "新几内亚"], ["py", "巴拉圭"], ["pe", "秘鲁"], ["ph", "菲律宾"], ["pl", "波兰"], ["pt", "葡萄牙"], ["qa", "卡塔尔"], ["ro", "罗马尼亚"], ["ru", "俄罗斯"], ["rw", "卢旺达"], ["kn", "圣基茨和尼维斯"], ["vc", "圣文森特和格林纳丁斯"], ["lc", "圣卢西亚"], ["ws", "萨摩亚"], ["sm", "圣马力诺"], ["st", "圣多美和普林西比"], ["sa", "沙特"], ["sn", "塞内加尔"], ["rs", "塞尔维亚"], ["sc", "塞舌尔"], ["sl", "塞拉利昂"], ["sg", "新加坡"], ["sk", "斯洛伐克"], ["si", "斯洛文尼亚"], ["sb", "所罗门群岛"], ["so", "索马里"], ["ss", "南苏丹"], ["za", "南非"], ["es", "西班牙"], ["lk", "斯里兰卡"], ["sd", "苏丹"], ["sr", "苏里南"], ["sz", "斯威士兰"], ["se", "瑞典"], ["ch", "瑞士"], ["sy", "叙利亚"], ["tj", "塔吉克斯坦"], ["tz", "坦桑尼亚"], ["th", "泰国"], ["tl", "东帝汶"], ["tg", "多哥"], ["to", "汤加"], ["tt", "特立尼达和多巴哥"], ["tn", "突尼斯"], ["tr", "土耳其"], ["tm", "土库曼斯坦"], ["tv", "图瓦卢"], ["ug", "乌干达"], ["ua", "乌克兰"], ["uy", "乌拉圭"], ["uz", "乌兹别克斯坦"], ["vu", "瓦努阿图"], ["ve", "委内瑞拉"], ["cv", "佛得角"], ["vn", "越南"], ["ye", "也门"], ["zm", "赞比亚"], ["zw", "津巴布韦"], ["tw", "台湾"], ["va", "梵蒂冈"]]
                for co in cou:
                    if co[0]==location.lower():
                        location=co[1]
                print(id,'  ',tron_wallet_addr,'  ',location,'  ',begin)
                tables.write(begin, 0, id)
                tables.write(begin, 1, tron_wallet_addr)
                tables.write(begin, 5, location)
                begin+=1
                excel.save(now_time+'_other.xls')
                sleep(1)
