from scapy.all import fuzz,TCP,IP,sr#构造TCP扫描
ans,unans = sr(IP(dst="192.168.1.1")/fuzz(TCP(dport=80,flags="S")),timeout=1)#使用IP(),TCP()创建数据包，fuzz()填充数据包
for s,r in ans:
    if r[TCP].flags==18:
        print("This port is Open")