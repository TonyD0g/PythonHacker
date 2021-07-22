#coding:utf-8
import threading
import paramiko
import subprocess
def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())#设置自动添加和保存目标ssh服务器的ssh密钥
    client.connect(ip, username=user, password=passwd)#连接
    ssh_session = client.get_transport().open_session()#打开会话

    if ssh_session.active:#如果会话存在，则执行相关的指令
        ssh_session.exec_command(command)#执行命令
        print(ssh_session.recv(1024)) #返回命令执行结果(1024个字符)
    return
def main():#此段代码可修改为    用户能控制输入的ip,user,passwd,command的值
    ip="192.168.0.1"
    user='whoiam'
    passwd='what'
    command='ping www.baidu.com'
    ssh_command(ip,user,passwd,command)


if __name__ == "__main__":
    main()
