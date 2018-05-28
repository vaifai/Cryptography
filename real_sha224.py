from struct import pack,unpack
from array import array
from string import join
A,B,C,D,E,F,G,H=0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939, 0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4

def rotate(n,b):
    return (((n >> b) & 0xffffffff) | ((n & 0xffffffff) << (32 - b))) & 0xffffffff
def enc(x):
   return join([chr(i) for i in x], '').encode('hex')

def compress(chunk):
    global A,B,C,D,E,F,G,H
    a,b,c,d,e,f,g,h=A,B,C,D,E,F,G,H
    k = (
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
            )

    w=[]
    print h
    for i in range(0,64,4):
        w.append(unpack('>I', enc(chunk[i:i+4]).decode('hex'))[0])
    for i in range(16,64):
        temp1=rotate(w[i-15],7) ^ rotate(w[i-15],18) ^ (w[i-15] >> 3)
        temp2=rotate(w[i-2],17) ^ rotate(w[i-2],19) ^ (w[i-2] >> 10)
        w.append((w[i-16]+temp1+temp2+w[i-7])% 2**32)
    for i in range(64):
        s1=rotate(e,6) ^ rotate(e,11) ^ rotate(e,25)
        ch=(e & f) ^ ((~e) & g)
        temp1=(h+s1+ch+k[i]+w[i])% 2**32
        s0=rotate(a,2) ^ rotate(a,13) ^ rotate(a,22)
        maj= (a & b) ^ (a & c) ^ (b & c)
        temp2=(s0+maj)% 2**32
        h=g
        g=f
        f=e
        e=(d+temp1)% 2**32
        d=c
        c=b
        b=a
        a=(temp1+temp2)% 2**32

    A,B,C,D,E,F,G,H=(A+a)% 2**32,(B+b) % 2**32,(C+c)% 2**32,(D+d)% 2**32,(E+e) % 2**32,(F+f)% 2**32,(G+g)% 2**32,(H+h)% 2**32
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
h=['']*8
ans=''
h[0],h[1],h[2]=hex(A),hex(B),hex(C)
h[3],h[4],h[5],h[6],h[7]=hex(D),hex(E),hex(F),hex(G),hex(H)
for i in range(7):
    temp=h[i]
    ans+=temp[2:len(temp)-1]
print ans
    
