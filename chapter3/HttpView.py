#coding:utf-8
import socketserver
import re
from socket import *
DataPack="""
GET http://detectportal.firefox.com/canonical.html HTTP/1.1
Host: detectportal.firefox.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Cache-Control: no-cache
Pragma: no-cache
Connection: keep-alive
"""


addr = ("127.0.0.1",8080)
def getHost(DataPack):#获取DataPack里的host
    result = re.search(r'Host:\s(.*?)\s'.encode(),DataPack)#正则表达式
    host = result.group(1)
    return host

class Myproxy(socketserver.BaseRequestHandler):
    def handle(self):
        self.HttpRqst = self.request.recv(1024)#获取http请求
        self.Rhost = getHost(self.HttpRqst)#获取远程主机
        newSock = socket(AF_INET,SOCK_STREAM)#建立TCP连接
        newSock.connect((str(self.Rhost),80))#80端口连接
        newSock.send(self.HttpRqst)#发送数据
        buffer = []#buffer缓冲区
        while True:
            d = newSock.recv(1024)
            if d:
                buffer.append(d)
            else:
                break
        self.HttpRspn = "".join(buffer)#.encode()
        self.request.sendall(self.HttpRspn)

if __name__ =="__main__":
    server = socketserver.ThreadingTCPServer(addr,Myproxy)
    server.serve_forever()
