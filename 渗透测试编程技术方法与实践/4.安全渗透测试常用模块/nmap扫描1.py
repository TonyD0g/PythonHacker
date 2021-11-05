import nmap

target = "192.168.0.1"
port = "80"
nm = nmap.PortScanner()
nm.scan(target, port)
for host in nm.all_hosts():  # 遍历host
    print('----------------------------------------------------')
    print('Host : {0} ({1})'.format(host, nm[host].hostname()))  # 输出ip.目标主机名称
    print('State : {0}'.format(nm[host].state()))  # 端口状态
    for proto in nm[host].all_protocols():  # 输出该ip的所有协议，和协议状态
        print('----------')
        print('Protocol : {0}'.format(proto))
        lport = list(nm[host][proto].keys())
        lport.sort()  # 从小到大排列
        for port in lport:
            print('port : {0}\tstate : {1}'.format(port, nm[host][proto][port]['state']))
