import itertools

words = "1234568790abcdefghijklmnopqrstuvwxyz"  # 字典来源词汇
temp = itertools.permutations(words, 2)  #随机挑选两个元素组成字典
passwords = open("dic.txt", "a")
for i in temp:#输出到文本文件中,每行一个
    passwords.write("".join(i))
    passwords.write("".join("\n"))
passwords.close()
