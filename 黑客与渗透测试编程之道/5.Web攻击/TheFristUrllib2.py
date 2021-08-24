#-*- coding:utf8 -*-
#发起get请求
import urllib2
try:
    body = urllib2.urlopen("http://www.360.cn")
    print(body.read())
except urllib2.URLError, e:
    print(e.code)