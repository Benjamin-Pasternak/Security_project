from Crypto.Util.number import getPrime
from functools import lru_cache
import numpy as np 
import sys
from mongo import mongodb_atlas_test
#from monggo import *
import hashlib

"""
(n,e) = public_key
(n,d) = private_key
p, q = large prime numbers 
phi = (p - 1) * (q - 1) = totient function 
d = mod_inv_euclid_extended(e, phi)
-----------
we keep d and n locally, and hidden in a file or something 
we push n and d to the mongo server 
"""

def gen_p_q():
    while True:
        p = getPrime(512)
        q = getPrime(512)
        if p != q:
            return p, q

def gen_n(p, q):
    return p * q

def gen_phi(p, q):
    return (p - 1) * (q - 1)

def gen_e(phi):
    e = 3
    while e < phi:
        if gcd_euclid(e, phi) == 1:
            return e
        e += 1

@lru_cache(maxsize=None) 
def gcd_euclid(a, b):
    if b == 0:
        return a
    return gcd_euclid(b, a % b)

@lru_cache(maxsize=None)
def gcd_euclid_extended(a, b):
    if b == 0:
        return 1, 0, a
    x, y, d = gcd_euclid_extended(b, a % b)
    return y, x - (a // b) * y, d

@lru_cache(maxsize=None)
def mod_inv_euclid_extended(a, m):
    x, y, d = gcd_euclid_extended(a, m)
    if d == 1:
        return x % m
    return None

def gen_d(e, phi):
    return mod_inv_euclid_extended(e, phi)

def encrypt_block(m, e, n):
    return pow(m, e, n)

def decrypt_block(c, d, n):
    return pow(c, d, n)

def rsa_encrypt_message(m, e, n):
    blocks = [int(x) for x in str(m)]
    c = []
    for block in blocks:
        c.append(encrypt_block(block, e, n))
    return c

def rsa_decrypt_message(c, d, n):
    blocks = [int(x) for x in c]
    m = []
    for block in blocks:
        m.append(decrypt_block(block, d, n))
    return m


"""
--------------------------------------------------------------------------------
---------------------------- This is for the signup ----------------------------
--------------------------------------------------------------------------------
"""
def gen_public_key():
    p, q = gen_p_q()
    n = gen_n(p, q)
    phi = gen_phi(p, q)
    e = gen_e(phi)
    return (n, e), e
def gen_private_key(n, e):
    d = gen_d(e, n)
    return (n, d)

database = mongodb_atlas_test()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password):
    public_key, e = gen_public_key()
    private_key = gen_private_key(public_key[0], e)
    print(public_key)
    print(private_key)
    with open('keys.txt', 'w') as f:
        f.write(str(public_key) + '\n')
        f.write(str(private_key))
    # hash the password since we don't want server to know the password 
    # is this safer to do on our end or server end?
    database.insert_user({'username': username, 'password' : hash_password(password), 'public key' :public_key })
    
    
    

def main():
    p, q = gen_p_q()
    n = gen_n(p, q)
    phi = gen_phi(p, q)
    e = gen_e(phi)
    d = gen_d(e, phi)
    print('THE JOKE IS ON YOU')
    n = 121543145891208210636432592820358575166897868744597769703199475916233427367488688963263007727958174734511591057599153099042046121780789193412468225070481448574695099996303228561669434914612021614545600419827717844058217396781962020194666880805897141128264131999243581998796411571384967202839260199279651585227
    e = 3
    d = 81028763927472140424288395213572383444598579163065179802132983944155618244992459308842005151972116489674394038399435399361364081187192795608312150046987632383130066664202152374446289943074681076363733613218478562705478264521308013463111253870598094085509421332829054665864274380923311468559506799519767723485
    m = int.from_bytes(b'hi', 'big')
    # print(m)
    c = rsa_encrypt_message(m, e, n)
    print(c)
    m2 = rsa_decrypt_message(c, d, n)
    print(m2)
    m2 = int(''.join([str(x) for x in m2]))
    #m2 = int(m2)
    m2 = m2.to_bytes((m2.bit_length() + 7) // 8, 'big').decode('utf-8')
    print(m2)
    # b = m2.to_bytes(, 'big')
    # b = b.decode('utf-8')
    # print(b)
    




if __name__ == '__main__':
    main()


    

