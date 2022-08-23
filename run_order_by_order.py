import os

path = "D:\\"
name = "getbalance.py"

run_files = []

for root , dirs , files in os.walk(path , topdown = False):
    for name in files:
        file = os.path.join(root, name)
        if name in file:
            run_files.append(root)

run_files = set(run_files)
# print(run_files)

for file in run_files:
    os.chdir(file)
    os.popen(f"python {name}")
