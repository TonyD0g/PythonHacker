#   -*- coding:utf8 -*-
#   web站点地图爬取
#   将保存好的web文件根据需要整理出对渗透有利的文件
"""
1.首先我们定义远程目标网站及用来下载和解压网站对应的Web应用的本地目录，同时列出不感兴趣的文件后缀名清单
2.web_paths变量是我们的Queue对象，它用来存储那些我们试图在远程服务器上定位的文件
3.之后，使用os.walk函数遍历本地Web应用目录下的所有文件和目录，在我们遍历所有文件和目录的同时，创建目标网站
  的全部文件路径，同时通过清单过滤出我们想要的文件，对找到的合法文件都添加到web_paths_Queue中。
4.源代码底部，创建了一批线程，每一个都由test_remote的函数发起.
5.test_remote函数运行在一个循环中以保证程序持续运行直到web_paths Queue为空。
6.每次迭代中，都从Queue对象中获取一个路径，添加到目标网站的主路径中，同时试图获取该文件
    如果能顺利获取到文件，就输出HTTP状态码并给出文件的全路径
7.如果文件没有找到或者被.htaccess文件保护，将会弹出一个错误信息，自动处理错误并保证循环继续执行.

"""
import Queue
import threading
import os
import urllib2

threads = 10

target = "http://192.168.1.105/Joomla/"
directory = "./Joomla/"
filters = ["jpg", ".gif", ".png", ".css"]

os.chdir(directory)
web_paths = Queue.Queue()

for r,d,f in os.walk("."):
    for files in f:
        remote_path = "%s%s" % (r,files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not  web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()

            print("[%d] => %s" % (response.code, path))
            response.close()

        except urllib2.HTTPError as error:
            print("Failed %s" % error.code)
            pass

for i in range(threads):
    print("Spawning thread %d" % i)
    t = threading.Thread(target=test_remote)
    t.start()