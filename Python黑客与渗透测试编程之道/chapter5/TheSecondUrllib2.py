#-*- coding:utf8 -*-
#发起post请求，post和get请求的区别是一个可携带参数，一个不可以
import urllib2
url = "http://www.360.cn/"
headers={}
# Googlebot －＞ google爬虫
headers['User-Agent'] = "Googlebot"

request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)

print(response.read())
response.close()