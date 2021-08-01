#coding:utf-8
#配套资料：https://www.cnblogs.com/piperck/p/5572756.html
""""
IP类中的__new__方法将原始缓冲区中的数据（在这个例子中是我们从网络中接受到的数据）填充到结构中，
当调用__init__方法时，__new__方法已经完成了对数据缓冲区中数据的处理。
在__init__方法中，我们对数据进行了内部处理，输出了可读性更强的协议类型和IP地址

"""
import socket
import os
import struct#解码用,结构体数据结构
from ctypes import *#解码用
import threading
import time
import sys
from netaddr import IPNetwork, IPAddress



def main():
    # -*- coding:utf8 -*-



    # 监听主机，即监听那个网络接口，下面的ip为我的kali的ip
    host = "10.10.10.145"

    # 扫描的目标子网
    # subnet = "192.168.1.0/24"
    # 没有命令行参数,默认192.168.1.0/24
    if len(sys.argv) == 1:#实现从程序外部向程序传递参数 如例子1：python scanner.py 192.168.1.10
        subnet = "192.168.1.0/24"
    else:
        subnet = sys.argv[1]#即传入例子1的 192.168.1.10

    # 自定义的字符串,我们将在ICMP响应中进行核对
    magic_message = "PythonRule!"
    #“icmp是Internet控制报文协议。它是TCP/IP协议簇的一个子协议，
    # 用于在IP主机、路由器之间传递控制消息。控制消息是指网络通不通、主机是否可达、路由是否可用等网络本身的消息。”
    def udp_sender(subnet, magic_message):# 参数：内网ip,报文信息。函数作用：批量发送UDP数据包。
        time.sleep(5)  # 可以说程序暂停5秒吧
        # 建立一个socket对象(SOCK_DGRAM:UDP客户端)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for ip in IPNetwork(subnet):#如果该ip在内网中
            try:
                # 函数作用：尝试发送magic_message这个消息到子网的每个ip,还用了个不怎么可能用的65212端口
                sender.sendto(magic_message, ("%s" % ip, 65212))
            except:
                pass  # 代表什么也不做

    class IP(Structure):# ip头定义
        _fields_ = [
            ("ihl", c_ubyte, 4),  # ip head length:头长度
            ("version", c_ubyte, 4),  # 版本
            ("tos", c_ubyte),  # 服务类型
            ("len", c_ushort),  # ip数据包总长度
            ("id", c_ushort),  # 标识符
            ("offset", c_ushort),  # 片偏移
            ("ttl", c_ubyte),  # 生存时间
            ("protocol_num", c_ubyte),  # 协议数字,应该是协议类型,这里用数字来代表时哪个协议,下面构造函数有设置映射表
            ("sum", c_ushort),  # 头部校验和
            ("src", c_ulong),  # 源ip地址
            ("dst", c_ulong)  # 目的ip地址
        ]

        # __new__(cls, *args, **kwargs)  创建对象时调用，返回当前对象的一个实例;注意：这里的第一个参数是cls即class本身
        def __new__(self, socket_buffer=None):#socket_buffer:它代表一个要发送或处理的报文，并贯穿于整个协议栈
            return self.from_buffer_copy(socket_buffer)
            #使用from_buffer_copy方法在__new__方法将收到的数据生成一个IP class的实例

        # __init__(self, *args, **kwargs) 创建完对象后调用，对当前对象的实例的一些初始化，无返回值,即在调用__new__之后，根据返回的实例初始化；注意，这里的第一个参数是self即对象本身【注意和new的区别】
        def __init__(self, socket_buffer=None):#__init__方法初始化一部分数据保存到对应的实例属性值中
            self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}# 协议字段与协议名称的对应

            # 可读性更强的ip地址(转换32位打包的IPV4地址为IP地址的标准点号分隔字符串表示。)
            self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
            self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

            # 协议类型
            try:
                self.protocol = self.protocol_map[self.protocol_num]
            except:
                self.protocol = str(self.protocol_num)

    class ICMP(Structure):#ICMP头定义
        #
        _fields_ = [
            ("type", c_ubyte),  # 类型
            ("code", c_ubyte),  # 代码值
            ("checksum", c_ubyte),  # 头部校验和
            ("unused", c_ubyte),  # 未使用
            ("next_hop_mtu", c_ubyte)  # 下一跳的MTU
        ]

        def __new__(self, socket_buffer):
            return self.from_buffer_copy(socket_buffer)

        def __init__(self, socket_buffer):
            pass

    if os.name == "nt":#如果是windoes系统，则可嗅探所有协议的数据，如果不是
                        #则说明使用的是Linux系统，Linux系统只支持嗅探ICMP数据
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)  # raw的中文是生的意思,大概就是原始套接字的意思吧
    #创建套接字
    sniffer.bind((host, 0))  # 这里端口为0,监听所有端口吧~

    # 设置在捕获的数据包中包含IP头
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # 在Windows平台上,我们需要设置IOCTL以启用混杂模式
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # 开启多线程发送udp数据包
    t = threading.Thread(target=udp_sender, args=(subnet, magic_message))
    t.start()

    try:#检查ICMP响应是否来自于我们的目标子网，最后确认ICMP信息中是否包含我们自定义的字符串签名，如果都满足，
        #则输出产生这个ICMP数据的主机的IP地址。
        while True:
            # 读取数据包
            raw_buffer = sniffer.recvfrom(65565)[0]

            # 将缓冲区的前20个字节按IP头进行解析,如果不解析的话信息都为打包的二进制形式，非常难以理解
            ip_header = IP(raw_buffer[0:20])#切片操作

            # 输出协议和通信双方IP地址
            print  ("Protocol: %s %s ->  %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))

            # 如果为ICMP,进行处理
            if ip_header.protocol == "ICMP":

                # 计算ICMP包的起始位置,并获取ICMP包的数据
                offset = ip_header.ihl * 4  # ihl是头部长度,代表32位(即4字节)长的分片的个数 [我的理解是因为一个字节表示一个符号,所以这里的offset要搞成以字节为单位的,为的是下一句的提取数据]
                buf = raw_buffer[offset:offset + sizeof(ICMP)]

                # 解析ICMP数据
                icmp_header = ICMP(buf)

                # print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code)

                # 检查类型和代码值是否都为3，为3说明该ip所代表的计算机存在，向发送方回传了一个ICMP报文
                if icmp_header.type == 3 and icmp_header.code == 3:
                    # 确认响应的主机再我们的目标子网之内
                    if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                        # 确认ICMP包中包含我们发送的自定义的字符串
                        if raw_buffer[len(raw_buffer) - len(magic_message):] == magic_message:
                            print(   "Host Up: %s" % ip_header.src_address)




    # 处理CTRL-C
    except  KeyboardInterrupt:

        # 如果运行再Windows上,关闭混杂模式
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)  # -*- coding:utf8 -*-


if __name__ == "__main__":
    main()