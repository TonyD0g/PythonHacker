import nmap
nm = nmap.PortScanner()
nm.scan(hosts='192.168.1.0/24',arguments='-sP')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
for host, status in hosts_list:
    print(host+" is "+status)