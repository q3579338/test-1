import os

path = "D:\\"
run_file_name = "1.py"

run_files = []

for root , dirs , files in os.walk(path , topdown = False):
    for name in files:
        file = os.path.join(root, name)
        if run_file_name == name:
            #print(file)
            run_files.append(root)

run_files = set(run_files)
#print(run_files)

for file in run_files:
    os.chdir(file)
    # try:
    os.popen(f"python {run_file_name} > {run_file_name}.log")
    # except Exception as e:
    #     print(e)
