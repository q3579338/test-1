import os
from multiprocessing import Pool
from time import sleep

path = "D:\\"
run_file_name = "1.py"

run_files = []

for root , dirs , files in os.walk(path , topdown = False):
    for name in files:
        file = os.path.join(root, name)
        if run_file_name == name:
            # print(file)
            run_files.append(root)

run_files = set(run_files)
# print(run_files)

def run(name , i):
    #print(f"sleep {i}")
    sleep( i * 5)
    os.chdir(name)
    res = os.popen(f"python {run_file_name} > {run_file_name}.log")
    res = res.read()

if __name__ == "__main__":
    #print(len(run_files))
    p = Pool(len(run_files))

    index = 1
    for file in run_files:
        p.apply_async(run , args = (file,index,))
        print(index)
        index+=1

    p.close()
    p.join()