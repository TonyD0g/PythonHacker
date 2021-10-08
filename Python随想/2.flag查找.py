j = 0
s = input('Please input the string\n')
for i in s:
    if s.find('f') >= 0 and s.find('l') >= 0 and s.find('a') >= 0 and s.find('g') >= 0:
        print("Maybe have flag!")
        j = 1
        exit(0)

if j == 0:
    print("don't find \'flag\'")
