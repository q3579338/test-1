# -*- coding: UTF-8 -*-
import os
import re
from time import sleep

while True:
    address='INPUTADDRESS'
    result=os.popen('btfs/bin/btfs wallet balance').readlines()
    BttWalletBalance=''
    for data in result:
        pat='"BttWalletBalance":[0-9]+([.]{1}[0-9]+){0,1}'
        BttWalletBalance=re.search(pat,data)
        if BttWalletBalance!=None:
            BttWalletBalance=BttWalletBalance.group(0)
    BttWalletBalance=BttWalletBalance[19:]
    print(BttWalletBalance)
    add="btfs/bin/btfs wallet transfer "+address+" "+BttWalletBalance
    os.popen(add)
    sleep(10)
