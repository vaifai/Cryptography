const=[0x0000000000000001,0x0000000000008082,0x800000000000808A,0x8000000080008000,0x000000000000808B, 0x0000000080000001, 0x8000000080008081, 0x8000000000008009, 0x000000000000008A, 0x0000000000000088, 0x0000000080008009, 0x000000008000000A, 0x000000008000808B, 0x800000000000008B, 0x8000000000008089, 0x8000000000008003, 0x8000000000008002, 0x8000000000000080, 0x000000000000800A, 0x800000008000000A, 0x8000000080008081, 0x8000000000008080, 0x0000000080000001, 0x8000000080008008]

r=[[0,    36,     3,    41,    18]    ,
       [1,    44,    10,    45,     2]    ,
       [62,    6,    43,    15,    61]    ,
       [28,   55,    25,    21,    56]    ,
       [27,   20,    39,     8,    14]    ]

def rotate(x,n):
    n=n%64
    return ((x>>(64-n))+(x<<n)%(2**64))
    
def Round(A,fixed):
#Initialisation of temporary variables
        B=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        C= [0,0,0,0,0]
        D= [0,0,0,0,0]

        #Theta step
        for x in range(5):
            C[x] = A[x][0]^A[x][1]^A[x][2]^A[x][3]^A[x][4]

        for x in range(5):
            D[x] = C[(x-1)%5]^rotate(C[(x+1)%5],1)

        for x in range(5):
            for y in range(5):
                A[x][y] = A[x][y]^D[x]

        #Rho and Pi steps
        for x in range(5):
          for y in range(5):
                B[y][(2*x+3*y)%5] = rotate(A[x][y], r[x][y])

        #Chi step
        for x in range(5):
            for y in range(5):
                A[x][y] = B[x][y]^((~B[(x+1)%5][y]) & B[(x+2)%5][y])
        #Iota step
        A[0][0] = A[0][0]^fixed
        return A
            
def table(string):
    w=64
    tab=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for x in range(5):
        for y in range(5):
            offset=2*((5*y+x)*w)//8
            s2,temp=string[offset:offset+16],''
            for k in range(8):
                ind=(7-k)*2
                temp+=s2[ind:ind+2]
            tab[x][y]=int(temp,16)
    return tab


def absorb(string):
    #global const
    w=64#1600/25
    s=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    string+='00'*(512/8)
    for i in range(0,len(string)*4,1600):
        tab=table(string)
        for x in range(5):
            for y in range(5):
                s[x][y]=s[x][y] ^ tab[x][y]
        for x in range(24):
            tab=Round(tab,const[x])
    return tab

def convert(tab):
    temp=['']*25
    for i in range(5):
        for j in range(5):
            lane = (("%%0%dX" % 16) % tab[i][j])
            t=''
            for k in range(8):
                off=(7-k)*2
                t+=lane[off:off+2]
            temp[5*j + i]=t
    return ''.join(temp)
    
s=raw_input()
st=s.encode('hex')
length,rate=len(st)*4,1088
nbytes,pad_str,l=length/8,'',length%rate

##Padding

if(l==1080):
    pad_str+=st[0:nbytes*2]+'81'
else:
    pad_str+=st[0:nbytes*2]+'01'
    while((len(pad_str)*4)%rate < 1080):
        pad_str+='00'
    pad_str+='80'

##Padding Ends
tab=absorb(pad_str)
##Squeezing

out,ll='',256
while(ll>0):
    string=convert(tab)
    out=out+string[:1088/4]
    ll-=1088
    if(ll>0):
        tab=absorb(tab)
print out[:256/4].lower()
        
