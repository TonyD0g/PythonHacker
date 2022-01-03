#coding:utf-8
import requests

if __name__ == "__main__":
    #如何爬取图片数据
    url = "https://fanyi-cdn.cdn.bcebos.com/static/translation/img/header/logo_e835568.png"
    #content返回的是二进制形式的图片数据
    #text (字符串) content (二进制)  json() (对象)
    img_data = requests.get(url=url).content

    with open("./sb.png","wb") as fp:
        fp.write(img_data)




