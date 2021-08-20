import socket
s1 = socket.socket()
s1.bind(("127.0.0.1",2345))
s1.listen(5)
str="Hello world"
while 1:
    conn,address = s1.accept()
    print ("a new connect from",address)
    conn.send(str.encode())
    conn.close()