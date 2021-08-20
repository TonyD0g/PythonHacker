#-*- coding:utf8 -*-  
#类似于御剑后台扫描之类的软件，枚举法破解
import urllib2  
import threading  
import Queue  
import urllib  
  
threads = 50  
target_url = "http://testphp.vulnweb.com"  
wordlist_file = "./all.txt"  
resume = None   #作者说用于网络中断时，延续上一个尝试的字符串，而不用从头开始，这里好像没用到  
user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"  
  
  
def built_wordlist(wordlist_file): #读入字典文件
    fd = open(wordlist_file, "rb")  
    raw_words = fd.readlines()  
    fd.close()  
  """
    读入一个字典文件，然后开始对文件中的每一行进行迭代。如果网络连接突然断开或者目标网站中断运行，则我们
    设置的一些内置函数可以让我们恢复暴力破解会话。这可以通过让resume变量接上中断前最后一个尝试暴力破解
    的路径来实现。整个字典文件探测完毕后，返回一个带有全部字符的Queue对象
  """
    found_resume = False
    words = Queue.Queue()  

    for word in raw_words: #开始迭代
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
  
def dir_bruter(word_queue, extentsions=None):#暴力破解函数，extentsions:额外扩展
  """
   dir_bruter函数接受用字典字符填充的Queue对象，这些字符要用于暴力破解及结合一个可选列表进行添加文件扩展名来
   测试。首先，测试当前字符是否存在文件扩展名，如果没有，那么我们把它当做远程Web服务器上的测试目录。如果有一批
   文件扩展名进行测试。
   如果接受到的响应码不是404就输出，因为这可能会泄露远程Web服务器上的一些耐人寻味的信息而不是只是一个“找不到文件”
   的错误。
   对
  """
    while not word_queue.empty():  
        attempt = word_queue.get() 

        attempt_list = []  #用于储存要尝试的url
        if "." not in attempt: #检查是否有文件扩展名，如果没有就是我们要爆破路径，否则爆破文件
            attempt_list.append("/%s/" % attempt)  
        else:  
            attempt_list.append("/%s" % attempt)  

        if extentsions:#如果我们想暴力破解扩展名
            for extentsion in extentsions:  
                attempt_list.append("/%s%s" % (attempt, extentsion))  
  
        #迭代我们要尝试的文件列表  
        for brute in attempt_list:  
            #构造url
            url = "%s%s" % (target_url, urllib.quote(brute))  
            #print url  
            try:  
                headers = {}  
                headers['User-Agent'] = user_agent  
                r = urllib2.Request(url, headers=headers)  
  
                response = urllib2.urlopen(r)  
                #print response.__dict__
                if len(response.read()):  
                    print("[%d] ＝＞　%s" % (response.code, url))
            #用ｅ接收URLError的信息 
            except urllib2.URLError,e:  
                # code属性存在，并且code不是404  
                if hasattr(e, 'code') and e.code != 404:  
                    print("!!! %d => %s" % (e.code, url))
                pass  
  
  
word_queue = built_wordlist(wordlist_file)  
extentsions = [".php", ".bak", ".orig",".inc"]  

#开启多线程扫描
for i in range(threads):  
    t = threading.Thread(target=dir_bruter, args=(word_queue, extentsions))  
    t.start()  
