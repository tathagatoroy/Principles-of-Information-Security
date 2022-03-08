''' code to construct a cpa secure cryptosystem using pseudo random functions '''
''' author : Tathagato Roy '''


#import the neccessary libraries
#prg is a random number generator
import sys
import numpy as np
import random 
import time 


GENERATOR = 73
PRIME  = 39041


''' function to generate seed of given size n '''
def generate_seed(n):
    seed = int(time.time())
    seed = bin(seed).replace('0b','')
    if len(seed) > n:
        seed = seed[:n]
    elif len(seed) < n:
        seed = seed.zfill(n)
    return seed



''' function f(x,g,p) = g^x mod p where x is source , g is the generator of the Multiplicative group Zp and p is some large prime such that p-1 is not a product of small primes '''
''' It is computationally hard to invert.The problem of inverting this function is popularly called Discrete Log '''
def modular_exponentiation(x,g,p):
    #apparently python natively supports fast modular exponentiation through passing an optional parameter p to pow()
    return pow(g,x,p)


''' this function uses to the above defined function to generate the random bits '''
''' the hardcore bit is the msb(x) of g^x mod p '''
''' x is in string format '''
''' given a n bit source it generates random n + 1 bits ''' 
''' return f(x,g,p) = g^x mod p | msb(x) '''
def H(x,g,p):
    int_x = int(x,2)
    res = bin(pow(g,int_x,p)).replace('0b','')
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

''' class which is a construction of a secure encryption  which is secure against cpa attacks '''
class Cpa_Encryption:

    
    ''' n is the security parameter '''
    def __init__(self,n):
        self.n = n


    ''' returns a n bit string randomly from an uniform distribution '''
    def generation(self):
        seed = generate_seed(min(self.n - 1,16))
        key = Pseudo_Random_Generator(seed,self.n)

        return key
    
    ''' returns a (r,s) cipher text given an input x and key k where r is an randomly generated string and s = (F_k(r) xor x) where F is a pseudo random function '''
    def encryption(self,k,x):
       
        seed = generate_seed(min(self.n - 1,16))
        r = Pseudo_Random_Generator(seed,self.n)
        res = Pseudo_Random_Function(k,r)
        s = ""
        for i in range(len(res)):
            if res[i] == x[i]:
                s = s + '0'
            else:
                s = s + '1'
        return (r,s)
    

    ''' upon given a ciphertext (r,s) and key k , returns the decrypted value of the ciphertext'''
    def decryption(self,k,r,s):
        res = Pseudo_Random_Function(k,r)
        m = ""
        for i in range(len(res)):
            if res[i] == s[i]:
                m = m + '0'
            else:
                m = m + '1'
        return m
    
n = int(input("Enter the security parameter of the Encryption system (Ideally more than 16) :     " ))
if n <= 16:
    print("n should be atleast 16")
    sys.exit(1)
Roy_Enc = Cpa_Encryption(n)
while(1):
    ans = input("if you want to try out a query press y else n : "  )
    if ans == 'n':
        print("Exiting ....")
        sys.exit(0)
    elif ans == 'y':
        x = input("Enter the {0} bit binary message : ".format(n))
        if len(x) != n:
            print("Size of message is wrong,exiting")
            sys.exit(1)
        #generate key
        k = Roy_Enc.generation()

        print("The generated Key is : {0}".format(k))

        #encryption 
        r,s = Roy_Enc.encryption(k,x)
        print("The ciphertext is given by ({0},{1})".format(r,s))

        #decryption
        m = Roy_Enc.decryption(k,r,s)
        print("The decrypted message is {0}".format(m))
        if m == x:
            print("The Encryption Decryption process looks valid")
        else:
            print("There is some error in the Encryption or Decryption")
    else:
        print("Wrong key pressed ....")
        sys.exit(1)





        
        



            
