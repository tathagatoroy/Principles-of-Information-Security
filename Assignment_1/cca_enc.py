''' code to create CCA secure system  using CPA secure system and MAC '''
''' author : Tathagato Roy '''


#import the neccessary libraries
import sys
import numpy as np
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
        q = n // 4 + 1
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
        q = n // 4 + 1
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
class CCA_Encryption:
    
    ''' n is the security parameter and initialise cpa and mac systems'''
    def __init__(self,n):
        self.n = n
        self.mac = MAC(self.n)
        self.cpa = Cpa_Encryption(self.n)
    
    ''' generate k1,k2 '''
    def generation(self):
        k1 = self.cpa.generation()
        k2 = self.mac.generation()
        return k1,k2

    ''' encryption '''
    def encryption(self,k1,k2,x):
        r1,s = self.cpa.encryption(k1,x)
        r2,tag = self.mac.mac(k2,r1 + s)
        return r1,s,r2,tag
    

    ''' decryption '''
    def decryption(self,k1,k2,r1,s,r2,tag):
        if self.mac.verify(k2,r2,tag,r1 + s) == 1:
            dec = self.cpa.decryption(k1,r1,s)
            return dec
        else : return '-1' 
    


    

   
n = int(input("Enter the security parameter of the Encryption system (Ideally more than 16) :     " ))
if n <= 16:
    print("n should be atleast 16")
    sys.exit(1)
cca = CCA_Encryption(n)
while(1):
    ans = input("if you want to try out a query press y else n : "  )
    if ans == 'n':
        print("Exiting ....")
        sys.exit(0)
    elif ans == 'y':
        x = input("Enter the message of length {0} : ".format(n))
        #check if the size of the message is at max 2^(n/4 -1) 
        if len(x) != n:
            print("The message is not of the right size ,exiting ...")
        k1,k2 = cca.generation()
        print("the two keys generated are : {0} , {1}".format(k1,k2))
        r1,s,r2,tag = cca.encryption(k1,k2,x)
        print("The ciphertext c is given by : {0} and the tag t is given by : {1} ".format(r1 + s,r2 + tag))
        dec = cca.decryption(k1,k2,r1,s,r2,tag)
        if dec == '-1' :
            print("decryption is not possible")
        else:
            print("The decrypted message is {0} ".format(dec))

    

    else:
        print("Wrong key pressed ....")
        sys.exit(1)




        