#coding:utf-8

from socket import *
s= socket(AF_INET,SOCK_STREAM)
s.bind(("",8080))#监听8080端口，8080端口是web服务器常用的端口
s.listen(1)
sock,addr = s.accept()
data = sock.recv(1024)
print(data.decode())#输出监听到的数据
sock.close()
s.close()