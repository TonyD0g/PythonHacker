"""
聚焦爬虫：爬取页面中指定的页面内容。
    - 指定url
    - 发起请求
    - 获取响应数据
    - 数据解析
    - 持久化存储

数据解析分类：
    - 正则表达式
    - bs4
    - xpath （***）

数据解析原理概述：
    - 解析的局部的文本内容都会在标签之间或者标签对应的属性中进行存储
    - 1.进行指定标签的定位
    - 2.标签或者标签对应的属性中存储的数据值进行提取（解析）

实例：
<div class="pic"
<a class="c-gap-left-middle recommend-item-a" href="/s?tn=request_24_pg&amp;wd=vim%E4%B8%8B%E4%B8%80%E9%A1%B5&amp;rsv_crq=6&amp;bs=python%20check_hostname%20requires%20server_hostname" title="vim下一页" target="_blank" style="margin-left:85px;">
vim下一页
</a>
</div>

ex= "<div class = "pic">.*?</div>" #正则表达式

"""