import binascii
s=raw_input()
scale=16
num_bits=8
temp=bin(int(s,scale))[2:].zfill(num_bits)
print temp,len(temp)
