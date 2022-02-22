filename = 'Ascii.txt'
file_obj = open(filename, "w",encoding='utf-8')

#   生成纯数字的字典
for i in range(256):
    file_obj.write(chr(i))
    file_obj.write("\n")

print('[+]  Success!')
file_obj.close()

