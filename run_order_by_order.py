import os
from multiprocessing import Pool

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

def run(name):
    os.chdir(name)
    os.popen(f"python {run_file_name} > {run_file_name}.log")

if __name__ == "__main__":
    p = Pool(8)

    index = 1
    for file in run_files:
        p.apply_async(run , args = (file,))
        print(index)
        index+=1

    p.close()
    p.join()