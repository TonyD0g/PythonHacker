import requests
url='http://www.baidu.com'
print("Testing %s"%url)
try:
    response=requests.head(url)#向服务器发送get请求
except:
    print("[-] No web server")
    response = None
if response!= None:
    print(response.headers)#获取服务器返回的页面信息