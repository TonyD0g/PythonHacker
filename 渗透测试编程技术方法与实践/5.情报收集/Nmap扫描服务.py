import sys#Nmap扫描目标主机开发的端口和服务
import nmap
if len(sys.argv) != 3:
    print('Usage:ServiceScan <IP>\n eg: ServiceScan 192.168.1.1')
    sys.exit(1)
target= sys.argv[1]
port= sys.argv[2]
nm = nmap.PortScanner()
nm.scan(target, port,"-sV")
for host in nm.all_hosts():
	for proto in nm[host].all_protocols():
        		lport = nm[host][proto].keys()
        		lport.sort()
        		for port in lport:
            			print ('port : %s\tproduct : %s' % (port,nm[host][proto][port]['product']))