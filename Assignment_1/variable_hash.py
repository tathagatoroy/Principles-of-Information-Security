''' code to create a variable length collision resistance hash function which using Merkle Damgard function on the fixed length collision resistance hash function '''
''' author : Tathagato Roy '''

#import the neccessary libraries
import sys
import numpy as np
import time
import random 
import math

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

        
        


    



n = int(input("Enter the value of n ,preferably less than 16 for the fixed hash : "))
if n >= 16:
    print("the value of n is too large,exiting due to less computational resources")
    sys.exit(1)
hash_func = Variable_Hash(n)

while(1):
    ans = input("if you want to try out a query press y else n : "  )
    if ans == 'n':
        print("Exiting ....")
        sys.exit(0)
    elif ans == 'y':
        message = input("Enter the variable bit message of length at most {0}  : ".format(2**n - 1))

        print("the hash value of {0} is {1}".format(message,hash_func.hash(message)))
    else:
        print("wrong key pressed,exiting")
        sys.exit(1)


