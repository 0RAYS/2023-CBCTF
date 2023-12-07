from Crypto.Util.number import *
from hashlib import *
m = getRandomNBitInteger(300)

def gen_prime(n):
    p = getPrime(n)
    while p % 4 == 1:
        p = getPrime(n)
    return p

p = gen_prime(128)
print(f'p = {p}')
a = pow(m,2,p**3)

print(f'a = {a}')

flag = 'CBCTF{' + sha256(str(m).encode()).hexdigest() + '}'


'''
p = 334032027984155099402863982848235447227
a = 6363500121827697008224968006879792916113549541401919095721781619316319436679204160344656454420382763358609215987320
'''