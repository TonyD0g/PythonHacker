s = '田由中人工大王夫井羊'  # 0123456789
code = input("请输入当铺密码：")
code = code.split(" ")
print("\n", code)
w = ''
for i in code:
    k = ""
    # print("\n", i)
    for j in i:
        k += str(s.index(j))
    # print("\n", k)
    w += chr(int(k))
print(w)
