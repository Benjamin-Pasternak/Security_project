import socket 
import threading
from Crypto.Util.number import getPrime
from functools import lru_cache
import numpy as np 
import sys 



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
            print("Error, wrong ip or port")
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