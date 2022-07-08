'''
Author: honus
Date: 2021-10-06 13:55:31
LastEditTime: 2021-10-08 08:26:44
LastEditors: honus
Description: move D:/ login failed xls to one folder  #running on windows
FilePath: /test/move_loginfailed_folder.py
'''

import os,xlrd,shutil

time='2021_06_10'
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)

def remove_file(old_path, new_path):
    print(old_path)
    print(new_path)
    mkdir(new_path)
    filelist = os.listdir(old_path)
    print(filelist)
    for file in filelist:
        if 'xls' not in file:
            continue
        src = os.path.join(old_path, file)
        dst = os.path.join(new_path, file)
        print('src:', src)
        print('dst:', dst)
        shutil.move(src, dst)

xls_files=[]
path='D:\\'
for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if time in file and '$' not in file:
            xls_files.append(file)

print(xls_files)

move_files=[]
for xls in xls_files:
    data=xlrd.open_workbook(xls,formatting_info=True)
    table=data.sheets()[0]
    Check_list=table.col_values(11)[1:]
    flag=False
    for check in Check_list:
        if 'loginfailed' in check:
            flag=True
            break
    if flag:
        move_files.append(xls)

move_path=[]
for move in move_files:
    key=move.split('\\')[-1]
    move=move.replace(key,'')
    print(move)
    move_path.append(move)

move_path=set(move_path)
print(move_path)
path=''
for path in move_path:
    new_path=path.replace('D:\\','D:\\1\\')
    remove_file(path,new_path)
