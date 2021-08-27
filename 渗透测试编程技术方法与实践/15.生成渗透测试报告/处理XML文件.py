"""
   编写渗透测试报告的目的：以通俗易懂的语言概括此次渗透测试，并交付于 委托人。
   内容摘要：高度精简的方式概括工作，不要用专业术语。应该以发现的漏洞作为切入点，结合用户的实际安全需求来完成
   编写报告包含的范围：1.全部测试写入 2.将发现问题的测试写入  （二选一，或两者结合）

   报告应包含的内容:
      WAPITI模型：
            W：进行渗透测试的原因
            A: 在渗透测试过程中使用的方法
            P：在渗透测试过程中发现的问题
            I: 这些发现问题给目标带来的影响
            T； 给目标提出改正的方案
            I:明确客户已经清楚了解报告的内容

（目前我暂时用不到，所以不做了解，下方是书中源代码，不做注释）
 XML详解：https://www.runoob.com/python/python-xml.html

"""
import xml.dom.minidom#XML:可扩展标记语言
DOMTree = xml.dom.minidom.parse("c:/test.xml")
collection = DOMTree.documentElement
#在集合中获取所有所有端口
ports=collection.getElementsByTagName("port")
#打印每个端口的详细信息
for port in ports:
   print("*****Port*****")
   if port.hasAttribute("portid"):
      print( "Portid : %s" % port.getAttribute("portid"))
   state = port.getElementsByTagName('state')[0]
   print ("The State is: %s" %  state.getAttribute('state'))
   service = port.getElementsByTagName('service')[0]
   print( "The Service is: %s" %  service.getAttribute('name'))