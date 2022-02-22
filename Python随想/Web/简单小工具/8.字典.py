filename = 'test.txt'
file_obj = open(filename, "w")

#   生成纯数字的字典
for i in range(0000, 9999):
    file_obj.write(str(i).zfill(4))
    file_obj.write("\n")

file_obj.close()
