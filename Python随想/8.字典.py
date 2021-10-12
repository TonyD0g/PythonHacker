filename = 'test.txt'
file_obj = open(filename, "w")

for i in range(0, 100):
    file_obj.write(str(i))
    file_obj.write("\n")

file_obj.close()
