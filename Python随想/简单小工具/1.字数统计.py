# 字数统计
s = input("Please input string!\n")
i = 0

try:
    while s[i] != '\0':
        i = i + 1
except:
    print("字数统计:", i)
