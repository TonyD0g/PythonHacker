"""
   如果一个客户端去连接这个隐藏的热点的时候，就会发送"Probe request" 类型的数据包，只需要找到目的
   地址（Destination) 为Broadcast,并且为“Probe request” 的数据包就可找到隐藏的SSID名称.

"""
from scapy.all import *
iface = "wlan0mon"
def handle_packet(packet):
   if packet.haslayer(Dot11ProbeReq) or \
      packet.haslayer(Dot11ProbeResp) or \
      packet.haslayer(Dot11AssoReq):
      print("Found SSID " + str(packet.info))
print("Sniffing on interface " + iface)
sniff(iface=iface, prn=handle_packet)