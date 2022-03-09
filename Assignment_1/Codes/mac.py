''' code to create MAC using pseudo random generator and pseudo random function '''
''' author : Tathagato Roy '''


#import the neccessary libraries
#prg is a random number generator
import sys
import numpy as np
import time
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
''' given a n bit source it generates random n + 1 bits ''' 
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


class MAC:
    ''' n is the security parameter '''
    def __init__(self,n):
        self.n = n
    
    ''' generates the key '''
    def generation(self):
        seed = generate_seed(min(self.n - 1,16))
        key = Pseudo_Random_Generator(seed,self.n)

        return key
    

    ''' generates the MAC '''
    def mac(self,k,x):
        # first padding for it to be multiple of n/4
        # padding the last part with 10*
        q = math.ceil(n / 4)
        if len(x) % q != 0:
            x = x + '1'
        while(len(x) % q != 0):
            x = x + '0'
        new_size = len(x)
        d = new_size / q   # new size must be a multiple of n/4
        #print(new_size / q)
        d = int(d)

        seed = generate_seed(min(self.n - 1,16))
        # generate a nbit random number but cut it to n//4 to get r
        r_big = Pseudo_Random_Generator(seed,self.n)
        r = r_big[:q]
        tag = ''
        for i in range(1,d + 1):
            # convert  i to n // 4 bit binary
            i_bin = bin(i).replace('0b','').zfill(q)
            #convert d to n // 4 bit binary
            d_bin = bin(d).replace('0b','').zfill(q)
            # m_i
            m_i = x[(i-1)*q : i*q]
            z_i = r + d_bin + i_bin + m_i
            t_i = Pseudo_Random_Function(k,z_i)
            tag = tag + t_i
        return r,tag

    ''' verifies the mac '''
    def verify(self,k,r,tag,x):
        ''' rerun the mac '''
        # first padding for it to be multiple of n/4
        # padding the last part with 10*
        q = math.ceil(n / 4) 
        if len(x) % q != 0:
            x = x + '1'
        while(len(x) % q != 0):
            x = x + '0'
        new_size = len(x)
        d = int(new_size / q)   # new size must be a multiple of n/4
        new_tag = ''
        for i in range(1,d + 1):
            # convert  i to n // 4 bit binary
            i_bin = bin(i).replace('0b','').zfill(q)
            #convert d to n // 4 bit binary
            d_bin = bin(d).replace('0b','').zfill(q)
            # m_i
            m_i = x[(i-1)*q : i*q]
            z_i = r + d_bin + i_bin + m_i
            t_i = Pseudo_Random_Function(k,z_i)
            new_tag = new_tag + t_i

        #check whether the two tag are the same
        if new_tag == tag:
            return 1
        else:
            return 0

   
n = int(input("Enter the security parameter of the Encryption system (Ideally more than 16) :     " ))
if n <= 16:
    print("n should be atleast 16")
    sys.exit(1)
mac = MAC(n)
while(1):
    ans = input("if you want to try out a query press y else n : "  )
    if ans == 'n':
        print("Exiting ....")
        sys.exit(0)
    elif ans == 'y':
        x = input("Enter the variable length message : ")
        #check if the size of the message is at max 2^(n/4 -1) 
        if float(len(x)) > pow(2,(n/4) - 1):
            print("Size of message is too long,exiting")
            sys.exit(1)
        #generate key
        k = mac.generation()
        print("The generated Key is : {0}".format(k))

        #MAC generation
        r,tag = mac.mac(k,x)
        print("The mac tag is given by ({0},{1})".format(r,tag))

        #verification 
        print("Verfiying the generated MAC")
        if mac.verify(k,r,tag,x) == 1:
            print("Succesfully Verified")
        else:
            print("Corruption happened")
        print("Changing the first bit of the message and seeing if the verifier can detect that.")
        x_new = list(x) #convert to list
        #modify the fist bit
        if x_new[0] == '0':
            x_new[0] = '1'
        else:
            x_new[0] = x_new[0] + '0'
        x_new = "".join(x_new) # reconvert to string
        print("The modified messages is " + x_new)
        if mac.verify(k,r,tag,x_new) == 1:
            print("The new message is succesfully verified,This is wrong,our system is not secure")
        else:
            print("The message has been tampered with,as expected")
    

    else:
        print("Wrong key pressed ....")
        sys.exit(1)




        