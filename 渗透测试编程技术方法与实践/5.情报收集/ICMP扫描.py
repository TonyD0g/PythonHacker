from scapy.all import sr,IP,ICMP
target="192.168.1.8"
ans,unans=sr((IP(dst= target)/ICMP()),timeout=2)
for snd,rcv in ans:
    print(rcv.sprintf("%IP.src% is alive"))