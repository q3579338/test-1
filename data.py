import xlrd
import xlwt
import os
import subprocess as sub
import re
i=0
data=xlrd.open_workbook("./data.xls")
table=data.sheets()[0]
# ip_list=table.col_values(0)
# password_list=table.col_values(1)
Privkey=table.col_values(0)                 #List
row=table.nrows

excel = xlwt.Workbook(encoding = 'utf-8')
tables = excel.add_sheet('key')
tables=excel.get_sheet(0)
# tables.write(0,0,'ip')
# tables.write(0,1,'password')
tables.write(0,0,'Privkey')
tables.write(0,1,'public_key_base64')
tables.write(0,2,'public_key_hex')
tables.write(0,3,'private_key_hex')
while row>i:
    Key=Privkey[i]
    print('第'+str(i+1)+'个'+Key)
    #print(Key)
    Key=Key.encode()
    pro=sub.Popen('D:\ledger-util.exe',stdin=sub.PIPE,stdout=sub.PIPE)
    pro.stdin.write(Key)
    out=pro.communicate()
    # #print(out)
    
    # out=[b'please input private key of account: account public key (base64) is: CAISIQOEQ+eaJXL5io4+DIaDnth3HsFlZ7YNbzWWp/RmzgIBBQ==\naccount public key (hex) is: 048443e79a2572f98a8e3e0c86839ed8771ec16567b60d6f3596a7f466ce02010547a7fc6230e4852273652fb521bda5074c595e18114023957cd8a0eaa667a65d\naccount private key (hex) is: 8248d17a143fffbbc14297764b894152c6bce85257c7baf2953ad923bd2bca21\n']
    #print(out[0])
    # print(out[1])
    public_key_base64=''
    public_key_hex=''
    private_key_hex=''
    dev_ledger=''
    pat='account public key \(base64\) is: [\s\S]*account public key \(hex\)'
    public_key_base64=re.search(pat,str(out[0]))
    if public_key_base64!=None:
        public_key_base64=public_key_base64.group(0)


    pat1='account public key \(hex\) is: [\s\S]*account private key \(hex\)'
    public_key_hex=re.search(pat1,str(out[0]))
    if public_key_hex!=None:
        public_key_hex=public_key_hex.group(0)

    pat2='account private key \(hex\) is: [\s\S]*'
    private_key_hex=re.search(pat2,str(out[0]))
    if private_key_hex!=None:
        private_key_hex=private_key_hex.group(0)

    print(public_key_base64[32:-26])
    print(public_key_hex[29:-27])
    print(private_key_hex[30:-3])
    # tables.write(i+1,0,ip_list[i])
    # tables.write(i+1,1,password_list[i])
    tables.write(i+1,0,Privkey[i])
    tables.write(i+1,1,public_key_base64[32:-26])
    tables.write(i+1,2,public_key_hex[29:-27])
    tables.write(i+1,3,private_key_hex[30:-3])
    excel.save('encode.xls')
    i=i+1
