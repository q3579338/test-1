import paramiko
import xlrd
import xlwt

class Getscreen:
    def read(self):
        data=xlrd.open_workbook("./all.xls",formatting_info=True)
        table=data.sheets()[0]
        self.ip_List=table.col_values(0)
        self.password_List=table.col_values(1)
        row=table.nrows
        return row

    def getip(self,n):
        self.ip=self.ip_List[n].strip('\n')
        self.password=self.password_List[n].strip('\n')

    def connect(self):
        count=0
        success=False
        max_test=3
        while count < max_test and not success:
            try:
                username='root'
                port= 22
                # print(self.ip)
                # print(self.password)
                #print('尝试第'+str(count+1)+'次登陆')
                client=paramiko.SSHClient()
                key=paramiko.AutoAddPolicy()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(self.ip, port, username=username, password=self.password,timeout=30)
                return client
            except:
                if count == max_test-1:
                    print('连接失败，开始下一个。。。')
                    return False
                else:
                    print('登陆失败，尝试重新登陆')
                    count +=1

    def createxcel(self):
        self.excel = xlwt.Workbook(encoding = 'utf-8')
        self.tables = self.excel.add_sheet('screen')
        self.tables=self.excel.get_sheet('screen')

    def write(self,k,countbtfs):
        self.tables.write(k,0,self.ip)
        self.tables.write(k,1,countbtfs)
        self.excel.save('count.xls')

if __name__=='__main__':
    getscreen=Getscreen()
    row=getscreen.read()
    k=0
    getscreen.createxcel()
    while k<row:
        print('当前在第'+str(k+1)+'/'+str(row)+'个')
        getscreen.getip(k)
        client=getscreen.connect()
        if not client:
            getscreen.write(k,'loginfailed')
            k+=1
            continue
        command='screen -ls'
        stdin,stdout,stderr=client.exec_command(command)
        res=stdout.readlines()
        countbtfs=0
        for name in res:
            if 'btfs' in name:
                countbtfs+=1
        print(countbtfs)
        getscreen.write(k,countbtfs)
        k+=1