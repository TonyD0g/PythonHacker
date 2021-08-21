import nmap
target="192.168.1.1"
nm = nmap.PortScanner()
nm.scan(target, arguments=' -sT')
for host in nm.all_hosts():
    print('----------------------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    print('State : %s' % nm[host].state()) 