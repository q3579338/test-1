import os
path='./'
all_list=os.listdir(path)
for data in all_list:
    os.rename(data,data.split('.')[-2])