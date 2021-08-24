import socket


def send_file_2_client(client_socket,clientAddr):
    #1.接收客户端需要下载的文件名
    file_name = client_socket.recv(1024)
    print("客户端(%s)需要下载的文件是：%s" % (str(clientAddr), file_name.decode('gbk')))

    #2.打开这个文件，读取数据
    #with as 方式以读的形式文件不存在就会新建
    file_content = None
    try:
        f = open(file_name,'rb')
        file_content = f.read()
        f.close()
    except Exception as ret:
        print("没有要下载的文件（%s）" % file_name)
    #3.发送文件的数据给客户端
    if file_content:
       client_socket.send(file_content)

def main():
    #1.创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #2.绑定本地信息
    tcp_server_socket.bind(("",7892))
    #3.让默认的套接字由主动变成被动
    tcp_server_socket.listen(128)
    #4.等待客户端的链接
    while True:
            client_socket,clientAddr = tcp_server_socket.accept()
            #5.调用发送文件函数，完成为客户端服务
            send_file_2_client(client_socket,clientAddr)
            #6.关闭套接字
            client_socket.close()
    tcp_server_socket.close()

if __name__ == "__main__":
    main()