"""
    web服务器有些私密页面应当是不能显示的，普通用户很难访问，但是黑客会设法去访问。
    如果程序员没有注意去隐藏这些页面，则很容易引发安全隐患。
    所以写个枚举常见的隐藏页面

"""
import urllib2,argparse,sys
def host_test(filename,host):
    file = "list.txt"
    bufsize = 0
    e = open(file,'a',bufsize)
    print("[+]Reading file %s",file)
    with open(filename) as f:
        locations =  f.readlines()
    for item in locations:#枚举
        target = host +"/" +item
        try:
            request = urllib2.Request(target)
            request.get_method = lambda : "GET"#GET方法
            response = urllib2.urlopen(request)
        except:
            print("[-] %s is invalid",str(target.rstrip('\n')))
            response = None
        if response ! = None:
            print("[+] %s is vaild",str(target.rstrip('\n')))
            details = response.info()
            e.write(str(details))
    e.close()

host_test(filename=,host=)