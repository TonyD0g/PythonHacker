import socket
s2 =socket.socket()
s2.connect(("127.0.0.1",2345))
#对传输数据使用encode函数处理，Python3不再支持str类型传输，需要转换为bytes类型
data=bytes.decode(s2.recv(1024))
s2.close()
print (data)