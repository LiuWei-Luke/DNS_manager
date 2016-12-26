import os
from ecdsa import SigningKey, NIST192p
from ecdsa import VerifyingKey, BadSignatureError
from ecdsa.util import randrange_from_seed__trytryagain
sk = SigningKey.generate()
vk = sk.get_verifying_key()

open("private.pem", "w").write(sk.to_pem())
open("public.pem", "w").write(vk.to_pem())

sk = SigningKey.from_pem(open('private.pem').read())
message = open('Desktop/DNS_manager/app/message.txt', 'rb').read()
sig = sk.sign_deterministic(message)
open('signature', 'wb').write(sig)

vk = VerifyingKey.from_pem(open("public.pem").read())
message = open("Desktop/DNS_manager/app/message.txt", 'rb').read()
sig = open("signature", "rb").read()

f=open("signature",'rb')  
f.seek(0,0)  
index=0  
for i in range(0,16):  
    print "%3s" % hex(i),
print  
for i in range(0,16):  
    print "%-3s" % "#",
print  
while True:  
    temp=f.read(1)  
    if len(temp) == 0:  
        break  
    else:  
        print "%3s" % temp.encode('hex'),  
        index=index+1  
    if index == 16:  
        index=0  
        print   
f.close()  

try:
    vk.verify(sig,message)
    print "good signature"
except BadSignatureError:
    print "bad signatur"
