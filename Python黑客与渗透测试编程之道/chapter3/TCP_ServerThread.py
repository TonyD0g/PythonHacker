#coding:utf-8
import socketserver#Socket多线程
class TestSocket(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        print("CilentMessage:",self.data.decode())
        self.msg = input("Message:")
        self.request.send(self.msg.encode())
if __name__ =="__main__":
    host = ''
    port = 6666
    addrinfo = (host,port)
    server = socketserver.ThreadingTCPServer(addrinfo,TestSocket)
    server.serve_forever()