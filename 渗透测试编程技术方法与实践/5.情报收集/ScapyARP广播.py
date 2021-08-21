#ARP广播
from scapy.all import srp,Ether,ARP
dst="192.168.1.1"
#dst:目的硬件地址,src:源硬件地址,src会自动设置为本机地址
# #dst=ff:ff:ff:ff:ff:ff，目的是将数据包发送到网络中的各个主机上
ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=dst),timeout=2)
for s,r in ans:
    print("Target is alive")
    print(r.sprintf("%Ether.src% - %ARP.psrc%"))