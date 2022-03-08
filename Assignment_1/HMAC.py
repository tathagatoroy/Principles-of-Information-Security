''' code to create a HMAC using varaible length Collision Resistance Function '''
''' author : Tathagato Roy '''

#import the neccessary libraries
import sys
import numpy as np
import time
import random 
import math




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
''' given a n bit sorce it generates random n + 1 bits ''' 
''' return f(x,g,p) = g^x mod p | msb(x) '''
def H(x,g,p):
    int_x = int(x,2)
    res = bin(pow(g,int_x,p)).replace('0b','')
    hardcore_bit = x[0]
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
''' checks whether a number n is prime in O(N^(0.5)) '''
def isprime(n):
    isprime = True
    for i in range(2,n):
        if i*i > n:
            break
        if n % i == 0:
            isprime = False
    return isprime

''' generates a nbit prime of the form 2q + 1 where q is prime '''
''' this a brute force approach so will only work with reasonable bit sized number like 16 bits'''
def generate_prime(n):
    print("generating a prime number of length {0} bits".format(n))
    primes = {}
    max_val = 2**n - 1
    for i in range(3,max_val + 1):
        # check whether i is prime 
        if isprime(i):
            primes[i] = 1
            z = ( i - 1 ) / 2
            if z in primes.keys():
                if i.bit_length() == n:
                    print("the prime generated is {0}".format(i))
                    return i 

''' function f(x,g,p) = g^x mod p where x is source , g is the generator of the Multiplicative group Zp and p is some large prime such that p-1 is not a product of small primes '''
''' It is computationally hard to invert.The problem of inverting this function is popularly called Discrete Log '''
def modular_exponentiation(x,g,p):
    #apparently python natively supports fast modular exponentiation through passing an optional parameter p to pow()
    return pow(g,x,p)

''' function to find prime factors of a number n'''
def factorise(n):
    print("computing prime factors of {0}".format(n))
    i = 2
    prime_factors = {}

    while (n > 1):
        if n % i == 0:
            prime_factors[i] = 1
            n = n / i
            while(n % i == 0):
                n = n / i
                prime_factors[i] += 1
            i += 1
        else:
            i += 1
    print("The generated prime factors are : ")
    print(prime_factors)
    return prime_factors 




''' find a generator of prime group p '''
def find_generator(p):
    print("finding the generator for prime {0}".format(p))
    prime_factors = factorise(p - 1)

    for i in range(1,p):
        is_generator = True
        for s in prime_factors.keys():
            if pow(i,int((p - 1)/s),p) == 1:
                is_generator = False
                break
        if is_generator == True:
            print("the generator is given by : {0}".format(i))
            return i 


''' class to create fixed length collision resistance hash '''
class Fixed_Hash:
    ''' generate the nbit prime,its generator and random h belonging Z*p '''
    def __init__(self,n):
        self.n = n 
        self.prime = generate_prime(n)
        self.generator = find_generator(self.prime)
        self.h = random.randint(1,self.prime-1)
        print(" the prime is {0} , generator {1} and h is {2}".format(self.prime,self.generator,self.h ))
    
    ''' x is a 2n bit string '''
    def hash(self,x):
        k = len(x)
        
        x1 = x[:int(k/2)]
        x2 = x[int(k/2):]
        int_x1 = int(x1,2)
        int_x2 = int(x2,2)
        g1 = pow(self.generator,int_x1,self.prime)
        h1 = pow(self.h,int_x2,self.prime)
        res = (g1 * h1) % self.prime
        return bin(res).replace('0b','').zfill(self.n)


''' class to create variable length collision resistance hash '''
class Variable_Hash:
    
    ''' intialise a fixed length hash  of parameter n '''
    def __init__(self,n):
        self.fixed_hash = Fixed_Hash(n)
    
    ''' hash function '''
    def hash(self,m):
        #compute the number of blocks
        b = math.ceil(len(m)/self.fixed_hash.n)
        #pad the message so it is exact multiple of b
        while(len(m) % self.fixed_hash.n != 0):
            m = m + '0'

        #initialise z_0 as 0^n    
        curr_z = ''
        for i in range(self.fixed_hash.n):
            curr_z += '0'
        
        for i in range(1,b+1):
            cur_x = m[(i - 1)*self.fixed_hash.n:i*self.fixed_hash.n]
            curr_z = self.fixed_hash.hash(curr_z + cur_x)
        L = bin(len(m)).replace('0b','').zfill(self.fixed_hash.n)
        return self.fixed_hash.hash(curr_z + L)

def string_xor(a,b):
    s = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            s = s + '0'
        else:
            s = s + '1'
    return s
        
''' class to construct a hmac '''
class HMAC:
    def __init__(self,n,iv=0, ipad=0x5c, opad=0x36):
        self.n = n
        self.iv = bin(iv).replace('0b','').zfill(n)
        self.ipad = bin(ipad).replace('0b','').zfill(n)
        self.opad = bin(opad).replace('0b','').zfill(n)
        ''' generate key '''
        seed = generate_seed(min(self.n - 1,16))
        self.k = Pseudo_Random_Generator(seed,self.n)
        self.Vhash = Variable_Hash(n)

        
    
    def Mac(self,x):
        v1 = string_xor(self.k,self.opad)
        v2 = string_xor(self.k,self.ipad)
        v3 = self.iv + v2 + x
        v4 = self.Vhash.hash(v3)
        v5 = self.iv + v1 + v4
        res = self.Vhash.hash(v5)
        return res
    
    def Verify(self,m,t):
        if self.Mac(m) == t:
            return 1
        else:
            return 0

n = int(input("Enter the size of the output hash (should be more than 16 and less than 30) :     " ))
if n < 16 or n >= 30:
    print("n should be more than 16 and less than 30")
    sys.exit(1)
hmac = HMAC(n)
while(1):
    ans = input("if you want to try out a query press y else n : "  )
    if ans == 'n':
        print("Exiting ....")
        sys.exit(0)
    elif ans == 'y':
        x = input("Enter the variable length message : ")
        #check if the size of the message is at max 2^(n/4 -1) 
        #if float(len(x)) > pow(2,(n/4) - 1):
            #print("Size of message is too long,exiting")
            #sys.exit(1)


        #HMAC generation
        res = hmac.Mac(x)
        print("The hmac tag is given by ({0})".format(res))

        #verification 
        print("Verfiying the generated HMAC")
        if hmac.Verify(x,res) == 1:
            print("Succesfully Verified")
        else:
            print("Corruption happened")
        

    else:
        print("Wrong key pressed ....")
        sys.exit(1)





