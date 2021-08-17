import socket
#python是胶水语言，因为他有很多 库，库：别人写好的代码
def main():
    #1.创建tcp的套接字
     tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #2.链接服务器
     server_ip = input("请输入要链接的服务器的ip:")
     server_port = int(input("请输入要链接的服务器的port:"))
     server_addr = (server_ip,server_port)
     tcp_client_socket.connect(server_addr)
   #  if tcp_client_socket.connect == "null":
      #  exit(0)
     while True:
            #3.发送数据/接收数据
            #因为是tcp,类似打电话，不用重复写端口和ip
            send_data = input("请输入要发送的数据:")
            if send_data == "null":
                print("进程已结束！\n")
                break
            tcp_client_socket.send(send_data.encode("gbk"))
    #4.关闭套接字
     tcp_client_socket.close()

if __name__ == "__main__":
    main()