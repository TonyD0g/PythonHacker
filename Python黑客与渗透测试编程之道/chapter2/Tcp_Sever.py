
import socket#套接字，插槽
def main():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#开启服务
    server.bind(("",7891))#开始监听端口
    server.listen(3)#允许的最大客户端连接数
    data, addr = server.accept()
    print("连接的客户端ip为：\t", addr)
    while True:
        Data=data.recv(1024).decode()
        print("服务器接受到的数据为：",Data)
        if Data.lower()=="null":
            print("服务器已关闭！\n")
            break



    #server.listen(5)

if __name__ == "__main__":
    main()