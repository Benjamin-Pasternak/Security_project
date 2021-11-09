import socket 
import threading
from Crypto.Util.number import getPrime
from functools import lru_cache
import numpy as np 
import sys 




def gen_p_q():
    return getPrime(512), getPrime(512)

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

def gcd_euclid_extended(a, b):
    if b == 0:
        return 1, 0, a
    x, y, d = gcd_euclid_extended(b, a % b)
    return y, x - (a // b) * y, d

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



def encryptMessage(message):
    p, q = gen_p_q()
    n = gen_n(p, q)
    phi = gen_phi(p, q)
    e = gen_e(phi)
    d = gen_d(e, phi)
    m = int.from_bytes(bytes(message,'utf-8'), 'big')
    
    c = rsa_encrypt_message(m, e, n)
    return str(c)
    


username = input("Enter username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
#connect client to server, local host
#TODO ask user for ip/port and not have it hard-coded in 
client.connect(('127.0.0.1', 5555))                             
#receive message
def receive_message():
    while True:                                                 
        #make connection, send username if applicable, else print message 
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'USERNAME':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        #error, wrong ip or port
        except:                                                 
            print("Error with connection, ip, or port")
            client.close()
            break
#write message
def write_message():
    while True:                                                 
        
        message = '{}: {}'.format(username, input(''))
        message2 = encryptMessage(message)
        client.send(message2.encode('utf-8'))

#reveive messages
receive_thread = threading.Thread(target=receive_message)               
receive_thread.start()
#send messages
write_thread = threading.Thread(target=write_message)                   
write_thread.start()