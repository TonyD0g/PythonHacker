# -*- coding:utf8 -*-
#   作用：针对目标创建一个合适的字典
from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import re
from datetime import datetime
from HTMLParser import HTMLParser


#   TagStripper 类允许我们去掉HTTP响应包中的HTML标签
class TagStripper(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.page_text = []

    #   遇到两个标签之间的数据时调用
    #   handle_data 函数将页面的文本内容存储到变量中
    def handle_data(self, data):
        self.page_text.append(data)

    #   遇到注释时调用
    #   将开发者注释的内容添加到字典中
    #   调用了handle_data 函数（以便我们在处理的过程中想改变处理页面的方式）
    def handle_comment(self, data):
        self.handle_data(data)

    #   Strip 函数将HTML 代码填充到HTMLParser 基类中，返回结果页面的文本内容
    def strip(self, html):
        # 会调用上面的两个函数
        self.feed(html)
        return "".join(self.page_text)


#   与之前的例子一样，我们的目标是在Burp的图像页面中添加右键菜单，
#   这里唯一的一个新的内容是需要将字典保存成集合(set)的形式,进而确保使用时不会有重复的词.

class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None
        self.hosts = set()
        # 我们初始化字典的集合并将它设置成最常用的密码：password ，保证它是字典中的最后一个词.
        # 按部就班,先设定一个非常常见的密码，因为是字典，不能重复最好，所以用集合
        self.wordlist = set(["password"])

        # 建立起我们的扩展工具
        callbacks.setExtensionName("Build Wordlist")
        callbacks.registerContextMenuFactory(self)

        return

    # 添加菜单
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Bulid Wordlist", actionPerformed=self.wordlist_menu))

        return menu_list

    #   现在我们添加逻辑控制，将选择的HTTP流量通过Burp转换成一个基本的字典.
    #   wordlist_menu函数处理点击菜单事件.
    def wordlist_menu(self, event):

        # 抓取用户点击细节
        http_traffic = self.context.getSelectedMessages()

        #   获取ip或主机名(域名)
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()
            #   它存储目标响应主机的名字.
            self.hosts.add(host)
            #   获取网站的返回信息
            http_response = traffic.getResponse()
            #   若有回应就调用get_word
            if http_response:
                #   然后检索HTTP响应的内容并发送给get_words函数.
                self.get_words(http_response)

        self.display_wordlist()
        return

    def get_words(self, http_response):

        headers, body = http_response.tostring().split("\r\n\r\n", 1)

        #   忽略下一个请求
        #   get_words函数去掉响应信息的HTTP头部，确保我们仅对响应的文本内容进行处理
        if headers.lower().find("content-type: text") == -1:
            return

        #   获取标签中的文本
        tag_stripper = TagStripper()
        #   TagStripper类将HTTP代码从剩下的页面文本中去除.
        page_text = tag_stripper.strip(body)
        #   我们使用正则表达式查找所有以字母开头后面跟着两个或者多个“单词”的字符
        #   匹配第一个是字母的，后面跟着的是两个以上的字母，数字或下划线／
        words = re.findall("[a-zA-Z]\w{2,}", page_text)


        for word in words:
            # 过滤长字符串
            if len(word) <= 15:
                #   完成最后的整理后，字符将以小写形式存储到字典(wordlist)中.
                self.wordlist.add(word.lower())

        return

    #   再后面添加更多的猜测
    #   mangle函数基于一些基本的密码生成“策略”将一个基础的单词转换成一类猜测密码。
    def mangle(self, word):
        #   在这个简单的例子中，我们创建了在基础单词上添加后缀的列表，包括当前的年份.
        year = datetime.now().year
        suffixes = ["", "1", "!", year]
        mangled = []
        #   做循环，将每个后缀添加到基础单词的后面.这样就创建了可尝试的新密码
        for password in (word, word.capitalize()):
            for suffix in suffixes:
                mangled.append("%s%s" % (password, suffix))

        return mangled

    def display_wordlist(self):
        #   输出用于生成密码字典的网站的名字
        #   处理每一个基础单词并输出结果
        print("#!comment: BHP Wordlist for site(s) %s" % ", ".join(self.hosts))

        for word in sorted(self.wordlist):
            for password in self.mangle(word):
                print(password)

        return

"""
    使用：
            1.在Burp中单击Extender标签，然后单击Add按钮，使用与之前扩展工具相同的步骤加载字典提取工具
        当加载完成后，使用浏览器访问网站。
            2.在Site Map面板中鼠标右键单击这个页面的URL并选择Spider this host 选项
            3.在Burp访问了目标网站的每一个链接之后，在界面右边顶端的区域选择所有的请求
              单击鼠标右键弹出菜单内容，选择Create Wordlist 选项
            4.现在检查扩展工具的输出栏，在现实环境中，我们想要将输出保存成文件
    
        现在，我们已经对一小部分的Burp API 进行了介绍，包括生成自己的攻击载荷和编写与Burp图形界面交互
    的扩展工具，在渗透测试的过程中，你经常会遇到特殊的问题或者有自动化的需求，Burp Extender API
    为你提供了解决问题的接口，至少可以把你从不同工具进行复制和粘贴数据的任务中解放出来。
        本章，我们展示了如何在Brup的工具库中建立出色的侦查工具。到目前为止，这个扩展工具仅将Bing搜索的
    前20个搜索结果检索出来，作为一个作业，你可以继续编写更多的请求以确保可以检索全部的结果，这需要你阅读
    一些Bing API文档并编写一些代码以处理大量的搜索结果，当然你还可以让Burp spider 爬取每一个新的站点
    或者自动化地搜索这些站点的漏洞.
"""