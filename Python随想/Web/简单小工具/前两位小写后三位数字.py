filename = 'test.txt'
file_obj = open(filename, "w")

str1 = 'qwertyuiopasdfghjklzxcvbnm'
str2 = '1234567890'
string1 = ''
string2 = ''
string3 = ''
y = 0


for i in str1:
    for x in str1:
        string1 = i + x
        string3 = string1
        while y<=999:
            string2 = str(y)
            string1 = string1 + string2
            if len(string1)==5:
                file_obj.write(str(string1))
                file_obj.write("\n")
                # print(string1)
            string1 = string3
            y = y + 1
        y = 0
print("已成功将字典写入到test.txt文件")
file_obj.close()
