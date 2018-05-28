from struct import pack,unpack
from array import array
from string import join
a,b,c,d=0x67452301,0xefcdab89,0x98badcfe,0x10325476

def F(x, y, z):
    return (x & y) | (~x & z)


def G(x, y, z):
    return (x & y) | (x & z) | (y & z)


def H(x, y, z):
    return (x ^ y ^ z)


def rotate(n, b):
    	return (((n << b) & 0xffffffff) | ((n & 0xffffffff) >> (32 - b))) & 0xffffffff

def enc(x):
   return join([chr(i) for i in x], '').encode('hex')


def compress(chunk):
    global a,b,c,d
    h=[0]*4
    h[0],h[1],h[2],h[3]=a,b,c,d
    string=[]
    for i in range(0,64,4):
        string.append(unpack('<I', enc(chunk[i:i+4]).decode('hex'))[0])

    s = (3,7,11,19)
    for r in xrange(16):
        i = (16-r)%4
        k = r
        h[i] = rotate( (h[i] + F(h[(i+1)%4], h[(i+2)%4], h[(i+3)%4]) + string[k]) % 2**32, s[r%4] )
    s = (3,5,9,13)
    for r in xrange(16):
        i = (16-r)%4 
        k = 4*(r%4) + r//4
        h[i] = rotate( (h[i] + G(h[(i+1)%4], h[(i+2)%4], h[(i+3)%4]) + string[k] + 0x5a827999) % 2**32, s[r%4] )
    s = (3,9,11,15)
    k = (0,8,4,12,2,10,6,14,1,9,5,13,3,11,7,15)
    for r in xrange(16):
        i = (16-r)%4 
        h[i] = rotate( (h[i] + H(h[(i+1)%4], h[(i+2)%4], h[(i+3)%4]) + string[k[r]] + 0x6ed9eba1) % 2**32, s[r%4] )
    a,b,c,d=a+h[0],b+h[1],c+h[2],d+h[3]

    
s=raw_input().strip()
pos=len(s) & 0x3fL
length=120-pos
if pos<56:
    length=56-pos
padded='\x80'+'\x00'*63
string=s+padded[:length]+pack('<Q',len(s)*8)
new_str=list(array('B',string))
print new_str
lim=len(new_str)
for i in range(0,lim,64):
    compress(new_str[i:i+64])
arr=[0]*4
arr[0],arr[1],arr[2],arr[3]=a,b,c,d
temp=''
for i in range(4):
    s=hex(arr[i])
    s=s[2:]
    for j in range(len(s)-3,-1,-2):
        temp+=s[j:j+2]
print temp

