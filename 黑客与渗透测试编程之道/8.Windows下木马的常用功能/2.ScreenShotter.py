#-*- coding:utf8 -*-
#   代码功能：   截取屏幕快照
"""
    我们使用PyWin32库，通过调用本地Windows API的方式实现抓屏功能.
    屏幕抓取器利用Windows 图形设备接口(GDI)获得抓取屏幕时必需的参数，如屏幕大小，分辨率等信息。
    一些抓屏软件只抓取当前活动额窗口或应用的图像。
"""
import win32gui
import win32ui
import win32con
import win32api

# 获取窗口桌面的句柄
hdesktop = win32gui.GetDesktopWindow()

# 获得显示屏的像素尺寸，它决定了屏幕快照的尺寸
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# 我们以之前获得的桌面句柄为参数，通过调用GetWindowDC函数创建设备描述表
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# 创建基于内存的设备描述表,用于储存我们捕获到的图片的数据，直到我们将二进制的位图保存到文件
mem_dc = img_dc.CreateCompatibleDC()

# 通过桌面设备描述标创建位图对象
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# 利用BitBlt函数将桌面图片按比特复制并保存在内存设备描述表中
# 你可以将这个过程看成是对GDI对象的memcpy调用
mem_dc.BitBlt((0,0), (width,height), img_dc, (left, top), win32con.SRCCOPY)

# 将位图保存到文件中
screenshot.SaveBitmapFile(mem_dc, "C:\\test.bmp")

# 释放对象
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())