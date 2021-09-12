# -*- coding:utf8 -*-
"""
    当你攻击一个Web服务器时，应该寻找这个Web服务器上所有域名，这样就能增加你获得Shell的机会
    微软的Bing搜索引擎能让你通过Bing查找在一个IP地址上运行的所有网站（使用IP搜索）
    Bing还会告诉你所查询域名的所有子域名（使用domain 关键字）.
    现在，我们当然可以通过工具向Bing提交查询并提交查询并导出HTML结果，但这其实是一种不好
    的行为（同时也违反了一些搜索引擎的使用规定）。
    为了避免不必要的麻烦，我们可以通过使用Bing API程序化的提交查询,解析我们想要的结果。在这个扩展工具
    中，我们不需要部署漂亮的Burp中，在Burp的目标范围内检测到任何URL都将每次查询的结果导入Burp中，
    在Burp的目标范围内检测到的任何URL都将被自动提取到列表中。因为我们已经介绍了如何阅读Burp API
    文档及如何将它们变成Python,所以接下来我们直接讲述代码.
"""
from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem
from java.util import List, ArrayList
from java.net import URL

import socket
import urllib
import json
import re
import base64

bing_api_key = "你的密钥"

"""
    这个类部署了基本的IBurpExtender接口和IContextMenuFactory，IContextMenuFactory
    允许我们在鼠标右键单击Burp中的请求时提供上下文菜单。
"""


class BurpExtender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self.context = None

        # 我们建立起扩展工具
        callbacks.setExtensionName("Use Bing")
        callbacks.registerContextMenuFactory(self)
        # 之后我们注册菜单句柄，这样我们就
        # 可以判定用户单击了哪个网站，从而完成Bing查询语句的构造。

        return

    # 创建菜单并处理点击事件，就是actionPerformed那里，点击调用bing_menu函数
    def createMenuItems(self, context_menu):
        self.context = context_menu
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Bing", actionPerformed=self.bing_menu))
        # 下个步骤是简历createMenuItem函数，
        # 该函数接受IContextMenuInvocation对象，用来判定用户选中了哪个HTTP请求。最后一个步骤用来
        # 渲染我们的菜单，并让我们的bing_menu函数处理点击事件。
        return menu_list

    def bing_menu(self, event):
        # 获取用户点击的详细信息
        #  当用户点击我们定义的上下文菜单时，bing_menu函数将被激活。我们接受所有高亮显示的HTTP请求
        #  然后检索每一个请求的域名部分并将它们发送到bing_search函数进行进一步处理。

        http_traffic = self.context.getSelectedMessages()

        print("%d requests highlighted" % len(http_traffic))

        # 获取ip或主机名(域名)
        for traffic in http_traffic:
            http_service = traffic.getHttpService()
            host = http_service.getHost()

            print("User selected host: %s" % host)

            self.bing_search(host)

        return

    def bing_search(self, host):
        # 检查参数是否为ip地址或主机名(域名)------使用正则
        is_ip = re.match("[0-9]+(?:\.[0-9]+){3}", host)
        #   bing_search函数首先判定我们传输的是否是IP地址或是域名
        # 若为ip
        if is_ip:
            ip_address = host
            domain = False
        else:
            ip_address = socket.gethostbyname(host)
            domain = True

        # 查寻同一ip是否存在不同虚拟机
        bing_query_string = "'ip:%s'" % ip_address
        self.bing_query(bing_query_string)

        # 若为域名则执行二次搜索，搜索子域名
        #
        if domain:
            bing_query_string = "'domain:%s'" % host
            self.bing_query(bing_query_string)

    def bing_query(self, bing_query_string):
        print("Performing Bing search: %s" % bing_query_string)
        # 编码我们的查询(如　urllib.quote('ab c')－－＞　'ab%20c')
        quoted_query = urllib.quote(bing_query_string)

        http_request = "GET https://api.datamarket.azure.com/Bing/Search/Web?$format=json&$top=20&Query=%s HTTP/1.1\r\n" % quoted_query
        http_request += "Host: api.datamarket.azure.com\r\n"
        http_request += "Connection: close\r\n"
        # 对API密钥使用base64编码
        http_request += "Authorization: Basic %s\r\n" % base64.b64encode(":%s" % bing_api_key)
        http_request += "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36\r\n\r\n"

        json_body = self._callbacks.makeHttpRequest("api.datamarket.azure.com", 443, True, http_request).tostring()

        # 去掉HTTP响应头，只取正文
        json_body = json_body.split("\r\n\r\n", 1)[1]

        # print json_body

        try:
            # 传递给json解析器
            r = json.loads(json_body)

            # 输出查询到的网站的相关信息
            if len(r["d"]["results"]):
                for site in r["d"]["results"]:
                    print("*" * 100)
                    print(site['Title'])
                    print(site['Url'])
                    print(site['Description'])
                    print("*" * 100)

                    j_url = URL(site['Url'])

            # 如果网站不在brup的目标列表中，就添加进去
            #   将Jython API和纯Python 组合添加到Burp扩展工具中，在攻击特定目标的时候
            #   用来做进一步的侦查非常使用.
            if not self._callbacks.isInScope(j_url):
                print("Adding to Burp scope")
                self._callbacks.includeInScope(j_url)

        except:
            print("No results from Bing")
            pass

        return

"""
    小试牛刀：
            使用与模糊测试扩展工具相同的步骤让Bing搜索工具运行起来，加载之后，通过网页浏览，
        之后在截获的GET请求上单击鼠标右键。如果扩展程序正确加载，你就可以看到右键菜单栏中显示
        出一个Send to Bing 选项
            当你单击这个选项后，根据加载扩展工具时选择的输出模式，就可以看到从Bing传回来的结果。
            (Extender 下的 Extensions)
        如果你在Burp单击  “Target” 标签并在之后选择“Scope“ 标签，你将看到新的域名已经被自动添加
        到目标库中，目标库中定义的目标仅限于用来攻击，爬取和扫描.
"""
