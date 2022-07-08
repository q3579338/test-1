import os
from time import sleep

os.system('screen -dmS btfs /root/btfs/bin/btfs daemon')
sleep(2)
os.system('screen -dmS zhuanzhang python3 /root/run.py')
sleep(2)