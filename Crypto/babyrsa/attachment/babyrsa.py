from Crypto.Util.number import *
from gmpy2 import *
from flag import flag
import math

def genprime():
    k = getRandomNBitInteger(64)
    p = 2023*k**5 + 2022*k**4 - 2023*k**3 - 2021*k**2 + 2020*k + 2019 + int(k**3*sin(k+2023)) - int(k**3*cos(k**2-2023)) + int(math.e**(23) * k)
    q = 2023*k**5 - 2022*k**4 + 2023*k**3 - 2021*k**2 + 2020*k - 2019 - int(k**2*sin(k*2023)) + int(k**2*cos(k**2*2023)) + int(math.e**(23) * k**2)
    p =next_prime(p)
    q =next_prime(q)
   
    return p,q

def encrypt(m,e,p,q):
    
    cp = pow(m,e,p)
    cq = pow(m,e,q)
    return cp,cq

m = bytes_to_long(flag)

p,q = genprime()
e = 65537
n = p*q
cp,cq = encrypt(m,e,p,q)

print(f'cp = {cp}')
print(f'cq = {cq}')
print(f'e = {e}')
print(f'n = {n}')

'''

cp = 2951478008429204122935337892738568379560198116832413976655842487911220583813451657632437020302109151
cq = 3042975941102854775825773171747972690767384220243723396259215468783407690302613940898320940464213373
e = 65537
n = 13226258685595630160447827442153267599814292160977306459359416297020102688049793771120158029953432640539514974565723831126909317859357612109049397896863392224521508922404189962829783829182814282953169

'''