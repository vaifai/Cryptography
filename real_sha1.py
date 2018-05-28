from struct import pack,unpack
from array import array
from string import join
import math

a,b,c,d,e=0x67452301,0xEFCDAB89,0x98BADCFE,0x10325476,0xC3D2E1F0

def enc(x):
   return join([chr(i) for i in x], '').encode('hex')

def rotate(n, b):
    	return (((n << b) & 0xffffffff) | ((n & 0xffffffff) >> (32 - b))) & 0xffffffff

def compress(chunk):
    global a,b,c,d,e
    h=[0]*5
    h[0],h[1],h[2],h[3],h[4]=a,b,c,d,e
    string=[]
    for i in range(0,64,4):
        string.append(unpack('>I', enc(chunk[i:i+4]).decode('hex'))[0])
    for i in range(16,80):
        string.append(rotate(string[i-3]^string[i-8]^string[i-14]^string[i-16] , 1))
    for i in range(80):
        f,k=None,None
        if(i<20):
            f=(h[1]&h[2])^(~h[1]&h[3])
            k=0x5A827999
        elif(i<40):
            f=h[1]^h[2]^h[3]
            k=0x6ED9EBA1
        elif(i<60):
            f=(h[1]&h[2]) ^ (h[1]&h[3]) ^ (h[2]&h[3])
            k=0x8F1BBCDC
        else:
            f=h[1]^h[2]^h[3]
            k=0xCA62C1D6
        temp=(rotate(h[0],5)+f+h[4]+k+string[i])% 2**32
        h[4]=h[3]
        h[3]=h[2]
        h[2]=rotate(h[1],30)
        h[1]=h[0]
        h[0]=temp
    a,b,c,d,e=h[0]+a,h[1]+b,h[2]+c,h[3]+d,h[4]+e
s=raw_input().strip()
pos=len(s) & 0x3fL
length=120-pos
if pos<56:
    length=56-pos
padded='\x80'+'\x00'*63
string=s+padded[:length]+pack('>Q',len(s)*8)
new_str=list(array('B',string))
print new_str
lim=len(new_str)
for i in range(0,lim,64):
    compress(new_str[i:i+64])
s1,s2,s3,s4,s5=hex(a%2**32),hex(b%2**32),hex(c%2**32),hex(d%2**32),hex(e%2**32)
print s1[2:len(s1)-1]+s2[2:len(s2)-1]+s3[2:len(s3)-1]+s4[2:len(s4)-1]+s5[2:len(s5)-1]
