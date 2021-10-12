    开发木马工具最大的挑战之一就是如何异步地进行控制，更新，以及如何从被控端接受数据.
因此，如何使用相对通用的方法将指令或代码推送到你的木马被控端就显得至关重要.
木马需要实现这样的灵活性，这不仅是因为你需要控制木马以完成各种不同的任务，
而且由于目标的操作系统存在差别，你可能需要针对不同的操作系统定制相应的功能代码.
    因此黑客发明了大量的命令和控制方法，其中一些非常具有创造性，如通过IRC甚至是Twitter进行控制,
在本章中，我们尝试将代码设计成服务，利用GitHub存储被控端的配置信息和窃取的数据,以及
被控端执行任务所需的各种模块代码等。我们还将探讨如何破解Python的原生库导入机制，这样
你在创建新的木马模块时，你的木马被控端能自动地从你的repo中获取和使用这些模块及相关的
依赖库。还有你需要注意你和GitHub之间的流量是否经过了SSL加密.


首先安装Python的GitHub API库，它可以让你自动地与你的repo进行交互，你可以在命令行下输入如下命令进行安装:
pip install github3.py 

然后安装git的客户端(图形或命令行的都行),下面的代码是基于Linux平台:
$ mkdir trojan
$ cd trojan
$ git init
$ mkdir modules
$ mkdir config
$ mkdir data
$ touch modules/.gitignore
$ touch config/.gitignore
$ touch data/.gitignore
$ git add .
$ git commit -m "Adding repo structure for trojan."
$ git remote add origin https://github.com/yourusername/chapter7.git
$ git push origin master