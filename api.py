from flask import Flask,request,jsonify
import logging,os

logging.basicConfig(format='%(asctime)s--%(levelname)s--%(message)s', level=logging.INFO)

app=Flask(__name__)

each=1
file1='1.txt'
file2='2.txt'

table={}
with open(file1,'r') as f:
    all_ip=[key.strip('\n') for key in f.readlines() if key!='\n']
with open(file2,'r') as f:
    tran_ip=[key.strip('\n') for key in f.readlines() if key!='\n']
all_ip_count=len(all_ip)
tran_ip_count=len(tran_ip)
if all_ip_count%each!=0:
    a=all_ip_count/each+1
else:
    a=all_ip_count/each
if a>tran_ip_count:
    logging.error('总ip与转发ip个数不符，请重新添加')
    os._exit(0)
flag=0
value=0
for key in all_ip:
    table[key]=tran_ip[flag]
    value+=1
    if value%each==0:
        flag+=1

@app.route('/<ip>',methods=['GET'])
def index(ip):
    try:
        return_ip=table[ip]
        return jsonify(return_ip)
    except:
        pass
    return 'False'
    
@app.route('/all')
def getall():
    return jsonify(table)
    
if __name__=='__main__':
    app.run(debug=True)