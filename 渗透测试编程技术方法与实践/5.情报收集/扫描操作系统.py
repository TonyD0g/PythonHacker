"""
    osmatch是一个字典类型，它包括'accuracy','line','osclass'三个键，而'osclass'中包含关键信息
    ，它本身也是一个字典类型，其中包含‘accuracy'(匹配度),’cpe'(通用平台枚举）,'osfamily'(系统类别）
    'osgen'(第几代操作系统），‘type’（设备类型），‘vendor'(生产厂家）6个键.


"""
import sys
import nmap
target=“192.168.169.133”
nm = nmap.PortScanner()
nm.scan(target, arguments="-O")
if 'osmatch' in nm[target]:
    for osmatch in nm[target]['osmatch']:
        print('OsMatch.name : {0}'.format(osmatch['name']))
        print('OsMatch.accuracy : {0}'.format(osmatch['accuracy']))
        print('OsMatch.line : {0}'.format(osmatch['line']))
        print('')
        if 'osclass' in osmatch:
            for osclass in osmatch['osclass']:
                print('OsClass.type : {0}'.format(osclass['type']))
                print('OsClass.vendor : {0}'.format(osclass['vendor']))
                print('OsClass.osfamily : {0}'.format(osclass['osfamily']))
                print('OsClass.osgen : {0}'.format(osclass['osgen']))
                print('OsClass.accuracy : {0}'.format(osclass['accuracy']))
                print('')