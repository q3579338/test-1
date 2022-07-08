import asyncio
import aiohttp
import xlrd
import xlwt
import json

data = xlrd.open_workbook("./data.xls",formatting_info=True)
table = data.sheets()[0]
Ids = table.col_values(0)
Ids = [k for k in Ids if k != '']

result = []

excel = xlwt.Workbook()
sheet = excel.add_sheet('data')
sheet.write(0 ,0 ,'Id')
sheet.write(0 ,1 ,'Version')
sheet.write(0 ,2 ,'UpTime')
sheet.write(0 ,3 ,'Status')
async def main():
    tasks=[]
    flag = 0
    for i in Ids:
        tasks.append(get_data(i , flag))
        flag+=1
    await asyncio.gather(*tasks)

async def get_data(id , index):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://scan-backend.btfs.io/api/v0/btfsscan/search/node_info?node_id={id}") as resp:
            version = await resp.text()

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://scan-backend.btfs.io/api/v1/btfsscan/host_score?node_id={id}") as resp:
            uptime = await resp.text()

    result.append((version , uptime , id , index))


if __name__ == '__main__':
    asyncio.run(main())
    result.sort(key = lambda x: x[3])
    flag = 1
    for i in result:
        try:
            verison = json.loads(i[0])
        except:
            pass

        try:
            uptime = json.loads(i[1])
        except:
            pass

        sheet.write(flag , 0 , i[2])
        if verison['code'] == 0:
            sheet.write(flag , 1 , verison['data']['version'])
        else:
            sheet.write(flag , 3 , 'Failed')
            flag += 1
            continue

        if uptime['code'] == 0:
            sheet.write(flag , 2 , uptime['data']['stats']['uptime'])
        elif uptime['code'] == 20:
            sheet.write(flag , 2 , '')
        else:
            sheet.write(flag , 3 , 'Failed')
            flag += 1
            continue

        flag += 1
    excel.save('result.xls')