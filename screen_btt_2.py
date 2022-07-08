'''
Author: honus
Date: 2022-01-20 22:02:49
LastEditTime: 2022-01-20 22:02:49
LastEditors: honus
Description: 
FilePath: \test\screen_btfs_2.py
'''
'''
Author: honus
Date: 2021-11-08 22:11:15
LastEditTime: 2022-01-20 21:45:41
LastEditors: honus
Description: 
FilePath: \test\screen.py
'''
import os
from time import sleep

lis=0
if lis==0:
    os.environ['BTFS_PATH'] = '/root/.btfs'
else:
    com='/root/.btfs'+str(lis)
    print(com)
    os.environ['BTFS_PATH'] = com
if lis==0:
    os.environ['PATH'] = '${PATH}:${HOME}/btfs/bin'
else:
    com='${PATH}:${HOME}/btfs'+str(lis)+'/bin'
    print(com)
    os.environ['PATH'] = com
if lis==0:
    com='btfs/bin/btfs daemon --chain-id 1029'
else:
    com='btfs'+str(lis)+'/bin/btfs daemon --chain-id 1029'
print(com)
os.system(com)