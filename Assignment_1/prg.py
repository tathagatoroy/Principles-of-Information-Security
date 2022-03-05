''' code to generate pseudorandom bits of size l(n) given n seed bits such l(n) > n '''
''' author : Tathagato Roy '''

#the generator for the given prime was computed using this tool http://www.bluetulip.org/2014/programs/primitive.html
GENERATOR = 73
PRIME  = 39041




#import the neccessary libraries
import sys
import numpy 

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
def G(x,g,p,L):
    start = x
    prn = ""
    for i in range(L):
        res = H(start,g,p)
        prn = prn + start[-1]
        start = res[:len(x)]
    return prn 







    


    






# take input seed size and the desired size of the pseudorandom output from the user 
seed_size = int(input("Please enter the size of the seed(Make sure its larger than 16 for safety and validity)\n"))
output_size = int(input("Please enter the desired size of the output\n"))

# ensure the size of output is greater than seed 
if seed_size >= output_size :
    print("output size must be greater than seed size") 
    sys.exit(1)
if seed_size < 16:
    print("Seed Size must be greater than 16")
    sys.exit(1)

#take the seed as input from user 
seed = input("Please enter a random seed\n")

#check whether the seed is the same size as advertized 
if len(seed) != seed_size:
    print("The size of the seed not the same as declared\n")
    sys.exit(1)

prn = G(seed,GENERATOR,PRIME,output_size)
print("The generated pseudo random number is {0} (in Binary) and {1} (in Decimal) and the size in bits is {2} from seed {3} (in decimal) and {4} (in binary)".format(prn,int(prn,2),len(prn),seed,int(seed,2)))


