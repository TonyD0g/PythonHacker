"""
    Wifi连接方式：
        客户端获取无线网络存在的方法时由客户端发送探测请求（probe requests),AP在接受到探测请求后
        会返回一个探测回应(Probe response) ,然后客户端会向AP发送一个认证（Authentication) 数据包，
        如果认证成功，客户端会发送关联请求（association request),AP在收到这个数据包之后，就会回复
        一个关联响应(association response).

   1.Dot11Beacon,这个类对应着Beacon信标帧.
   2.Dot11ProbeReq,这个类对应着Probe request数据帧。
   3.Dot11ProbeResp,对应着Probe response 数据帧
   4.Dot11AssoReq,  Association request 数据帧
   5.Dot11AssoResp, Association response 数据帧
   6.Dot11Auth,     Authentication 数据帧
   7.Dot11Deauth ,  Deauthentication 数据帧,解除认证，可以用来实现拒绝服务攻击.


"""
from scapy.all import *

interface = 'wlan0mon'  # 选择网卡
ap_list = []


def info(fm):
    if fm.haslayer(Dot11Beacon):  # 如果Beacon信标帧存在
        if fm.addr2 not in ap_list:
            ap_list.append(fm.addr2)
            print("SSID--> ", fm.info, "-- BSSID --> ", fm.addr2)


sniff(iface=interface, prn=info)
