#coding:utf-8
import requests

if __name__ == "__main__":
    #如何爬取图片数据
    url = "https://gimg0.baidu.com/gimg/src=https%3A%2F%2Fgameplus-platform.cdn.bcebos.com%2Fgameplus-platform%2Fupload%2Ffile%2Fimg%2Fd6dbddb2884f5ed2b002efb057f408d1%2Fd6dbddb2884f5ed2b002efb057f408d1.png&app=2000&size=f9999,10000&n=0&g=4n&q=90&fmt=jpeg?sec=0&t=8c1af48ab7efe53ee3f0a60cbacdb0dd"
    #content返回的是二进制形式的图片数据
    #text (字符串) content (二进制)  json() (对象)
    img_data = requests.get(url=url).content

    with open("./sb.png","wb") as fp:
        fp.write(img_data)

"""
1.今天花一个小时看菜鸟教程，极速入门
2.找到一个感兴趣的库，去搜它的玩法。
3.
"""


