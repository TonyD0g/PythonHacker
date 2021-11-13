import base64

s=''
with open('base.txt', 'r', encoding='UTF-8') as f:
    s=''.join(f.readlines()).encode('utf-8')
src=s
while True:
    try:
        src=s
        s=base64.b16decode(s)
        str(s,'utf-8')
        continue
    except:
        pass
    try:
        src=s
        s=base64.b32decode(s)
        str(s,'utf-8')
        continue
    except:
        pass
    try:
        src=s
        s=base64.b64decode(s)
        str(s,'utf-8')
        continue
    except:
        pass
    break
with open('result.txt','w', encoding='utf-8') as file:
    file.write(str(src,'utf-8'))
print("Decryption complete!")

