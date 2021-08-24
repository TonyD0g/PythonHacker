import socket
str_msg=input("请输入要发送信息：")
s2 =socket.socket()
s2.connect(("127.0.0.1",2345))
#对传输数据使用encode函数处理，Python3不再支持str类型传输，需要转换为bytes类型
str_msg=str_msg.encode(encoding='gbk')
s2.send(str_msg)
print (str(s2.recv(1024)))
s2.close()