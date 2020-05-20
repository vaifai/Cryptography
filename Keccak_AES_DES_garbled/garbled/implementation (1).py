import random
import intro as ff

kx,ky,kz=['']*2,['']*2,['']*2
#kz[0] for output 0 and kz[1] for output kz[1]
#kx will be input of first client and ky for second client

def gen_key():
    s=['']*2
    for i in range(2):
        temp=''
        for j in range(128):
            temp+=str(random.choice([0,1]))
        s[i]=temp
    return s[0],s[1]

def xor(a,b):
    s=''
    for i in range(128):
        if(a[i]=='0' and b[i]=='0'):
            s+='0'
        elif(a[i]=='1' and b[i]=='1'):
            s+='0'
        else:
            s+='1'
    return s

def send(tab,key1,key2,key3):
    print 'enter choice'
    print len(key1),len(key2),len(key3)
    num=input()
    s=ff.begin(num,key2[:128],key3[:128])
    n1,n2=key1[128],''
    if(s==key2[:128]):
        n2=key2[128]
    else:
        n2=key3[128]
    return xor(key1[:128],xor(s,tab[2*int(n1) + int(n2)]))

#Program starts Here. Generate random keys.    
kx[0],kx[1]=gen_key()
ky[0],ky[1]=gen_key()
kz[0],kz[1]=gen_key()
#Generate random bits r1 and r2
r1=random.choice([0,1])
r2=random.choice([0,1])
kx[0],kx[1],ky[0],ky[1]=kx[0]+str(0^r1),kx[1]+str(1^r1),ky[0]+str(0^r2),ky[1]+str(1^r2)
#print len(kx[0]),len(kx[1]),len(ky[0]),len(ky[1])
garb_tab=['']*4
for i in range(2):
    for j in range(2):
        #Here we are permuting entries in garbled table
        n1,n2=i^r1,j^r2
        if(i==0 or j==0):
            garb_tab[2*n1 + n2]=xor(kx[i],xor(ky[j],kz[0]))
        else:
            garb_tab[3]=xor(kx[1],xor(ky[1],kz[1]))
#sending garbled table
recv=send(garb_tab,kx[0],ky[0],ky[1])
if(recv==kz[0]):
    print '0'
elif(recv==kz[1]):
    print '1'
else:
    print 'malicious'
