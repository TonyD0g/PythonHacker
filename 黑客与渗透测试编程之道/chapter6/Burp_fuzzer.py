#-*- coding:utf8 -*-
#编写BurpSuite扩展
# 导入三个类，其中IBurpExtender类是编写扩展工具必须的类，后两个是Intruder的，我们就是要扩展它
from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator
from java.util import List, ArrayList

import random
"""
(1) 导入IBurpExtender类，这是编写Burp扩展的必须类，接着创建Intruder载荷生成器导入必要的类。

(2) 定义自己的BurpExtender类，他继承和扩展了IBurpExtender类和IIntruderPayloadGeneratorFactory类。

(3) 我们使用registerIntruderPayloadGeneratorFactory()函数注册BurpExtender类，
    这样Intruder工具才能生成攻击载荷。      

(4) getGeneratorName()函数返回载荷生成器的名称。

(5) createNewInstance()函数接收攻击相关的参数，返回IIntruderPayloadGenerator类型的实例，
    命名为BHPFuzzer。

"""
#定义自己的BurpExtender类，继承和扩展IBurpExtender和IIntruderPayloadGeneratorFactory类
class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        #用registerIntruderPayloadGeneratorFactory函数注册BurpExtender类，
        # 这样Intruder才能生成攻击载荷
        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    #返回载荷生成器的名称
    def getGeneratorName(self):
        return "BHP Payload Generator"

    # 接受攻击相关参数，返回IIntruderPayloadGenerator类型的实例，作者将他命名为BHPFuzzer
    def createNewInstance(self, attack):
        return BHPFuzzer(self, attack)
    """
    上述代码是扩展工具所需要的一个简单架构，它满足了BurpSuite对扩展工具的基本要求
    #以上函数中出现的莫名其妙的参数（如callbacks）皆是从IBurpExtender, IIntruderPayloadGeneratorFactory中继承的
    """



# 增加了max_payload(允许的最大payload数量), num_iterations(迭代次数)两个变量，用于控制模糊测试的次数
class BHPFuzzer(IIntruderPayloadGenerator):# 定义BHPFuzzer类，扩展了IIntruderPayloadGenerator类
    def __init__(self, extender, attack):
        self._extender = extender#extender参数属于IIntruderPayloadGenerator类自带的
        self._helpers = extender._helpers#_helpers参数属于IIntruderPayloadGenerator类自带的
        self._attack = attack#attack参数属于IIntruderPayloadGenerator类自带的
        self.max_payload = 10
        self.num_iterations = 0
        return

    # 通过比较判断迭代是否达到上限
    def hasMorePayloads(self):
        if self.num_iterations == self.max_payload:
            return False
        else:
            return True

    # 接受原始的HTTP负载，current_payload是数组，需要转化成字符串，传递给【模糊测试函数mutate_payload】
    def getNextPayload(self, current_payload):#current_payload参数属于IIntruderPayloadGenerator类自带的
        # 转换成字符串
        payload = "".join(chr(x) for x in current_payload)
        # 调用简单的变形器对POST请求进行模糊测试
        payload = self.mutate_payload(payload)
        # 增加FUZZ的次数
        self.num_iterations += 1
        return payload

    # 重置
    def reset(self):
        self.num_iterations = 0
        return

    def mutate_payload(self, original_payload):#original_payload参数属于IIntruderPayloadGenerator类自带的
        # 仅生成随机数或者调用一个外部脚本
        picker = random.randint(1,3)

        # 再载荷中选取一个随机的偏移量去变形
        offset = random.randint(0, len(original_payload)-1)
        payload = original_payload[:offset]

        # 在随机偏移位置插入SQL注入尝试
        if picker == 1:
            payload += "'"

        # 插入跨站尝试
        if picker == 2:
            payload += "<script>alert('xss');</script>"

        # 随机重复原始载荷
        if picker == 3:
            chunk_length = random.randint(len(payload[offset:]), len(payload)-1)
            repeater = random.randint(1,10)

            for i in range(repeater):
                payload += original_payload[offset:offset+chunk_length]


        # 添加载荷中剩余的字节，进行补全。AB 插入一个C =>   ACB
        payload += original_payload[offset:]

        return payload

    """
    (1) 定义自己的BHPFuzzer类，它扩展了IIntruderPayloadGenerator类。

    (2) 定义需要的类变量，添加max_payloads和num_payloads变量，
        他们用来对模糊测试的过程进行追踪，让Burp了解模糊测试完成的时间。

    (3) 部署hasMorePayloads()函数，该函数检查模糊测试时迭代的数量是否达到上限。

    (4)  getNextPayload()函数负责接收原始的HTTP载荷，这里是进行模糊测试的地方。

    (5) current_payload变量是数组模式，我们要将它变成字符串。

    (6) 将字符串传递给模糊测试的函数mutate_payload()

    (7) 将num_payloads变量的值增加，然后修改之后的载荷

    (8) 模糊测试函数

    """