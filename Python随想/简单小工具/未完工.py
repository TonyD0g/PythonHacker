# 两个为一组进行进制转换
i = 0
j = 0
s = input("Please input the string!\n")
try:
    while s[j] != '\0':
        j = j + 1
except:
    print("字数统计:", j)

string1 = ""
for x in range(j):
    y = s[i:i + 2]
    # print(type(y))
    try:
        string1 += str(chr(int(y, 16)))
    except:
        pass
    print(chr(int(y, 16)))

    i = i + 2

print(string1)
