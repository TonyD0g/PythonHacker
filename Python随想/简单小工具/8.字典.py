filename = 'test.txt'
file_obj = open(filename, "w")

#   生成纯数字的字典
for i in range(0, 100):
    file_obj.write(str(i))
    file_obj.write("\n")

file_obj.close()
