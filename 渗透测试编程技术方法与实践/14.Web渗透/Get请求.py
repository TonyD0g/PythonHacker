import requests
url= "http://www.baidu.com"
#构造Request数据包的头部
headers = {
 'Host':'www.baidu.com', 'User-Agent':'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive'
}
response = requests.get(url,headers)
print(response.text)