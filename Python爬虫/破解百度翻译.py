#utf-8
if __name__=="__main__":
    import requests
    import json
    url="https://fanyi.baidu.com/sug"#特定url

    headers={#UA伪装
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    while True:
        x = input("Please input you want to search the word:\n")
        data = {
            "kw": x#关键字替换
        }
        if x=="exit":
            exit()
        response=requests.post(url=url,data=data,headers=headers)
        dic_obj=response.json()#json()方法返回的是obj (如果确认相应数据的是json类)

        print(dic_obj)


    filename=x+".json"#文件名加后缀
    fp=open(filename,"w",encoding="utf-8")
    json.dump(dic_obj,fp=fp,ensure_ascii=False)
    #中文不允许 ASCII编码，所以ensure_ascii = false
    print("爬虫完成!\n")

