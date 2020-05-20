import random
import md5 as f1

#m0='010100000000111110100011101110111100110'
#m1='111100001010001011110011001100000001101'
def xor(s,m):
    length=max(128,len(m))
    ss,m0='',''
    msg=''
    for i in s:
        temp=bin(int(i,16))
        temp=temp[2:]
        l=4-len(temp)
        temp='0'*l + temp
        ss=ss+temp
    m0='0'*(length-len(m)) + m
    for i in range(length):
        if(ss[i]=='0' and m0[i]=='0'):
            msg+='0'
        elif(ss[i]=='1' and m0[i]=='1'):
            msg+='0'
        else:
            msg+='1'
    return msg

def sender(pk0r,C,r,q,m0,m1):
    mod=1000000007
    cr=pow(C,r,q)
    pk1r=float(cr*1.0)/float(pk0r)
    pkr0,pkr1=int(pk0r),int(pk1r)
    string1,string2=f1.pad(str(pkr0)),f1.pad(str(pkr1))
    h1,h2=f1.pri(string1),f1.pri(string2)
    msg0,msg1=xor(h1,m0),xor(h2,m1)
    return msg0,msg1
def find_gen(p,q):
    g=1
    while(g<p):
        if((pow(g,2,p)!=1) and (pow(g,q,p)!=1)):
            break
        g+=1
    return g
def begin(sig,m0,m1):
    p,q=999959,499979
    C=random.randrange(0,q+1,1)
    r=random.randrange(0,q+1,1)
    #print 'Enter choice of msg'
    #sig=input()
    gen=find_gen(p,q)
    pk=[0.0]*2
    pk[sig]=pow(gen,r,q)
    pk[1-sig]=float(pow(C,r,q)*1.0)/pk[sig]
    arr=['']*2
    arr[0],arr[1]=sender(pk[0],C,r,q,m0,m1)
    hashed=xor(f1.pri(f1.pad(str(int(pk[sig])))),arr[sig])
    return hashed
