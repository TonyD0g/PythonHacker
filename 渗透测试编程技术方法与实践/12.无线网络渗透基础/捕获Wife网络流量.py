from scapy.all import *
import subprocess
subprocess.call('airmon-ng start wlan0',shell=True)#进入网卡模式
iface = "wlan0mon"
def dump_packet(pkt):
   print(pkt.summary())#将捕获的流量输出出去.
while True:
    sniff(iface=iface,prn=dump_packet,count=10,timeout=3,store=0)