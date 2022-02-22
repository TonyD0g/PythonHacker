file1 = open("xrkRce.txt", "r+")

file2 = open("urls_export.txt", "r+")
# i =0
while 1:  # 按行读取文件并发起爬取
    line1 = file1.readline()
    if not line1:
        break
    file2.seek(0, 0)
    while 1:
        line2 = file2.readline()
        if not line2:
            break
        # line1 = "http://"+line1
        line1 = line1.replace('\n', '')
        line2 = line2.replace('\n', '')
        x = line2.find(line1)
        if x == -1:  # 即不非法，不处理该url
            pass
            # i = i +1
        else:  # 非法，处理该url
            print("[+]{} maybe have vuln".format(line1))

# print(i)
file1.close()
file2.close()
