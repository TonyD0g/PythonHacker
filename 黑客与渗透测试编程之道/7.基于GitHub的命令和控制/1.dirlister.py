# -*- coding:utf8 -*-
# 列出当前目录的所有文件,并作为字符串返回
import os


def run(**args):
    print("[*] In dirlister module.")

    files = os.listdir(".")
    return str(files)
