import socket
import xlrd
import xlwt

def detect_port(ip,port):
    """检测ip上的端口是否开放
    """
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        print('{0}:{1} is open'.format(ip,port))
        return True
    except:
        print('{0}:{1} is close'.format(ip,port))
        return False

if __name__ == '__main__':
    i=0
    port='221'
    data=xlrd.open_workbook("D:/Study/python/data.xls",formatting_info=True)
    excel = xlwt.Workbook()
    sheet = excel.add_sheet('ip')
    table=data.sheets()[0]
    ip_List=table.col_values(0)
    password_List=table.col_values(1)
    row=table.nrows
    while row>i:
        res=detect_port(ip_List[i], port)
        if res:
            sheet.write(i,0,ip_List[i])
        i=i+1
    excel.save('ipdata.xls')

