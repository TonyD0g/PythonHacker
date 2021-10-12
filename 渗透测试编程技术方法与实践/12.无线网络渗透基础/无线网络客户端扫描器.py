"""
    每一个无线设备在和AP连接时都需要向其发送一个ProbeReq数据包，而AP会返回一个ProbeResp 数据包
    这样只要捕获到网络中的所有ProbeReq数据包，就可以知道当前网络中有哪些设备连接到AP中.


"""
from scapy.all import *
import subprocess

subprocess.call('airmon-ng start wlan0', shell=True)
interface = 'wlan0mon'
probe_req = []


def probesniff(fm):
    if fm.haslayer(Dot11ProbeResp):
        if fm.addr2 not in probe_req:
            print("New Probe Request for: ", fm.info)
            print("The Probe is from MAC ", fm.addr2)
            probe_req.append(fm.addr2)


sniff(iface=interface, prn=probesniff)
