# -*- coding:utf8 -*-

import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private_key = ""

rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

chunk_size = 256
offset = 0
decrypted = ""
encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted += rsakey.decrypt(encrypted[offset:offset + chunk_size])
    offset += chunk_size

# 解压负载
plaintext = zlib.decompress(decrypted)

print(plaintext)

"""
小试牛刀:
    我们只需要在一个Windows主机上运行IE_exfil.py 脚本，然后等待它将数据成功提交到Tumblr站点上.
如果你在脚本中设置IE浏览器是可视的，那么你将看到上述整个流程。当这一切完成以后，你可以通过浏览Tumblr站点
的页面查看.
    查看页面发现一大块的加密数据，其隐含的是我们的文件名，然后将这块加密数据粘贴到你的解密脚本中.
缺点:在我们的IE_exfil.py脚本中,我们用空格字符补齐了最后256个字节，这将破坏某些文件的格式。
所以该项目另外一个需要改进的地方是将文件的原始大小加密存储到博客内容的开始处，这样你就可以在对齐文档之前
知道它的原始大小，从而在完成解密博客的内容之后，读入该文件的原始大小，将解密之后的文件调整到原长度.
"""
