i = 0
j = 0

s = input("Please input the string!\n")
try:
    while s[j] != '\0':
        j = j + 1
except:
    pass

string1 = ""
for x in range(j):
    y = s[i:i + 8]      # 8个8个分割
    # print(y,"\n")
    # print(hex(int(y,2)))
    #print(type(y))
    # y = str(y)
    # y = bin(int(y,16))
    string1 += y + ' '
    i = i + 8           # 8个8个分割,上面改了，这里也要改

print(string1)
