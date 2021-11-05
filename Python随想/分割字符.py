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
    y = s[i:i + 9]
    # print(y,"\n")
    string1 += y + ' '
    i = i + 9

print(string1)
