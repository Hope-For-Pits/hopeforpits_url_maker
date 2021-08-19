import cryptocode
import os,zlib,base64

key = os.environ['CURL_KEY']

curlcmd = base64.b64encode(zlib.compress(open('curl','rb').read()))
# print(curlcmd)

curl = cryptocode.encrypt(curlcmd.decode(),key)
print(curl)

curldec = cryptocode.decrypt(curl,key)
curlcmd = zlib.decompress(base64.b64decode(curldec)).decode()
# print(curlcmd)