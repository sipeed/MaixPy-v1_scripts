import hashlib

a = bytes([0]*65)
b = hashlib.sha256()
b.update(a)
b.update(a)
c = b.digest()
print(c)
if c != b"\xe5Z\\'sj\x87a\xc8\xe9j\xce\xc0r\x10#%\xe0\x8c\xb2\xd0\xdb\xb4\xd4p,\xfe8\xf8\xab\x07\t":
    raise(Exception("error! {}".format(c))) 

a = bytes([0]*1024)
b = hashlib.sha256(a)
c = b.digest()
print(c)
if c != b'_p\xbf\x18\xa0\x86\x00p\x16\xe9H\xb0J\xed;\x82\x10:6\xbe\xa4\x17U\xb6\xcd\xdf\xaf\x10\xac\xe3\xc6\xef':
    raise(Exception("error! {}".format(c))) 

print(c == b.digest()) # False here
