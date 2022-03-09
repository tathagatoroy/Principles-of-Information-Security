## Course : Principles of Information Security 

### Assignment 1

#### Name : Tathagato Roy
#### Roll number : 2019111020

Files : 
prg.py contains the construction of pseudo random generator where the user inputs the seed size n , seed (in binary string) and desired output size.

prf.fy : 
prf.fy contains the construction of pseudo random function, which maps n bit string to n bit string using pseudo random generator.

cpa_enc.py : 
cpa_enc.py contains the construction of cpa secure encryption scheme using pseudo random functions

mac.py : 
mac.py contains the construction of variable length Message Authentication Code using pseudo random functions

cca_enc.py : 
cca_enc.py contains construction of Chosen Ciphertext Attack secure encryption scheme using CPA secure encryption scheme and MAC.

fixed_hash.py : 
fixed_hash.py contains the construction of a fixed length collision resistant hash function which maps 2*n bit input to n bit output.

variable_hash.py : 
variable_hash.py contains the construction of a variable length collision resistant hash function constructed using merkle - damgard transformation on a fixed length collision resistant hash function

HMAC.py : 
This file contains the construction of a HMAC using variable length collision resistant hash function

All files contains detailed comments which explain how each part of code works.

to run any file run 
'''
python3 filename.py 
'''



