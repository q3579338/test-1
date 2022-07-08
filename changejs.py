import xlrd
import os,json
import xlwt

xls_files=[]

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file=os.path.join(root, name)
        if 'config.json' in file:
            xls_files.append(file)

print(xls_files)

for xls in xls_files:
    with open(xls,'r+') as f:
        data=f.readline()
        print(data)
        if data=='':
            continue
    try:
        with open(xls,'r+') as f:
            file=json.load(f)
            file['accelerate']=True
    except:
        continue
    with open(xls,'w+') as f:
        json.dump(file,f)





