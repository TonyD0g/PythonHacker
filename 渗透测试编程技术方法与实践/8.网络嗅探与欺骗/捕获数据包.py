from scapy.all import *
#sniff参数详解：https://blog.csdn.net/u010238483/article/details/105285644/
ip="192.168.1.1"
#这里ip的值尽量使用本机的IP地址，保证可以快速捕获到5个数据包
def Callback(packet):#回显函数
   packet.show()
packets=sniff(filter="host "+ip,prn=Callback,count=5)#prn:回显参数，filter:过滤规则
wrpcap("catch.pcap",packets)#保存为pcap文件