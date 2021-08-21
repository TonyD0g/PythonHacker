import nmap#使用Nmap进行ARP扫描
target="192.168.1.1"
nm = nmap.PortScanner()
nm.scan(target, arguments='-sn -PR')#-PR表示使用ARP,-sn表示只测试该主机的状态（为了加快扫描速度）
for host in nm.all_hosts():
    print('----------------------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    print('State : %s' % nm[host].state())