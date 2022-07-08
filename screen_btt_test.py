'''
Author: honus
Date: 2022-03-07 19:40:47
LastEditTime: 2022-03-07 19:42:08
LastEditors: honus
Description: 
FilePath: \test\screen_btt_test.py
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
    com='btfs/bin/btfs daemon --enable-gc --chain-id 199'
else:
    com='btfs'+str(lis)+'/bin/btfs daemon --enable-gc --chain-id 199'
print(com)
os.system(com)
