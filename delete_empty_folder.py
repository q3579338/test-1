'''
Author: honus
Date: 2021-10-10 17:04:25
LastEditTime: 2021-10-10 17:04:37
LastEditors: honus
Description: delete d:// folder with only getbalance
FilePath: /test/delete_empty_folder.py
'''
import os,shutil

xls_files=[]
key='getbalance'
path='D:\\'
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if key in file and '$' not in file:
            xls_files.append(file)

print(xls_files)

files=[]
for xls in xls_files:
    tmp=xls.split('\\')[-1]
    files.append(xls.replace(tmp,''))

files=list(set(files))
for file in files:
    print(file)
    res=os.listdir(file)
    if len(res)==1 and key in ''.join(res):
        shutil.rmtree(file)
        print('delete: ',file)
