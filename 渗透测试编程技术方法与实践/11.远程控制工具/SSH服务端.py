import subprocess
import socket
def run_command(command):
    # rstrip()用来删除string字符串末尾的指定字符（默认为空格）
    command=command.rstrip()
    print (command)
    try:
        child = subprocess.run(command,shell=True)
    except:
        child = 'Can not execute the command.\r\n'
    return child
s1 = socket.socket()
s1.bind(("127.0.0.1",2345))
s1.listen(5)
str="Hello world"
while 1:
    conn,address = s1.accept()
    print ("a new connect from",address)
    conn.send(str.encode(encoding='gbk'))
    data=conn.recv(1024)
    data=bytes.decode(data)
    print("The command is "+data)
    output = run_command(data)
conn.close()