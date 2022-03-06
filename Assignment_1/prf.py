''' code to generate pseudorandom function using pseudorandom generator '''
''' author : Tathagato Roy '''


#import the neccessary libraries
#prg is a random number generator
import sys
import numpy as np

GENERATOR = 73
PRIME  = 39041


''' function f(x,g,p) = g^x mod p where x is source , g is the generator of the Multiplicative group Zp and p is some large prime such that p-1 is not a product of small primes '''
''' It is computationally hard to invert.The problem of inverting this function is popularly called Discrete Log '''
def modular_exponentiation(x,g,p):
    #apparently python natively supports fast modular exponentiation through passing an optional parameter p to pow()
    return pow(x,g,p)


''' this function uses to the above defined function to generate the random bits '''
''' the hardcore bit is the msb(x) of g^x mod p '''
''' x is in string format '''
''' given a n bit source it generates random n + 1 bits ''' 
''' return f(x,g,p) = g^x mod p | msb(x) '''
def H(x,g,p):
    int_x = int(x,2)
    res = bin(pow(int_x,g,p)).replace('0b','')
    hardcore_bit = res[0]
    res = res.zfill(len(x)) # ensure res is same size as SEED SIZE by padding zeros
    return res + hardcore_bit

''' given a nbit seed, it generates a l bit random generator using the above define H function '''
def Pseudo_Random_Generator(x,L,g = GENERATOR,p = PRIME):
    start = x
    prn = ""
    for i in range(L):
        res = H(start,g,p)
        prn = prn + start[-1]
        start = res[:len(x)]
    return prn 

''' computes F(k,x) where F is a pseudo Random Function ,k is key and x is the input '''
''' k is a n bit string '''
''' if  x = x1x2x3....xn '''
''' F(k,x) = G_xn(G_xn-1(.....G_x1(k)) ...) '''
def Pseudo_Random_Function(k,x):
    start = k
    n = len(x) 
    for i in range(len(x)):
        res = Pseudo_Random_Generator(k,2*n)
        if x[i] == '0':
            start = res[:n]
        else:
            start = res[n:]
    return start
        



n = int(input("Enter the value of n(the security paramter)(should be greater than 16)  : "))

if n < 16:
    print("n should be greater than 16")
    sys.exit(1)

print("You can query the Pseudo Random Generator ")
while(1):
   
    r = input("Press y to continue and n to exit : ")
    if r == 'n':
        print("Exiting ....")
        sys.exit(0)
    elif r == 'y':
        k = input("Enter the value of Key : ")
        x = input("Enter the value of x : ")
        if len(k) != n:
            print("the size of Key should be equal to {0},please try again".format(n))
        elif len(x) != n:
            print("the size of x should be equal to {0},please try again".format(n))
        else:
            res = Pseudo_Random_Function(k,x)
            print("F({0},{1}) : {2}".format(k,x,res))
    else:
        print("wrong key pressed,exiting ....")
        sys.exit(1)
        






