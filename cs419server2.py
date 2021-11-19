import socket
import threading    
import sys                                            

#local host
host = '127.0.0.1'  
#unreserved port                                                   
port = 8081

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              
server.bind((host, port))                                               
server.listen(2)

#lists of clients accessing server and current usernames
clientList = []
usernameList = []

def send_message(message):                                                
    for client in clientList:
        client.send(message)

def get_usernameList():
    return usernameList


#client handler: receive and send client messages and check if they left. If left, then remove from lists
def client_handler(client):                                         
    while True:
        try:                                                            
            message = client.recv(1024)
            send_message(message)
        except:                                                         
            clientIndex = clientList.index(client)
            clientList.remove(client)
            client.close()
            username = usernameList[clientIndex]
            send_message('{} left'.format(username).encode('utf-8'))
            usernameList.remove(username)
            
            break

#receive clients, enter into clientList and usernameList
def receive():                                                          
    while True:
        client, address = server.accept()
        print("New user IP and Port: {}".format(str(address)))   

        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        username = username.replace(':', '')
        username = username.strip()
        usernameList.append(username)
        clientList.append(client)
        print("New user's username is {}".format(username))
        
        #TODO give each user unique id, probably set id to a counter
        
        send_message("New user {} joined".format(username).encode('utf-8'))
        client.send('You have connected to server'.encode('utf-8'))

        usernameList2 = 'USERLIST' + str(usernameList)

        print(usernameList2)
        
        send_message(usernameList2.encode('utf-8'))


        thread = threading.Thread(target=client_handler, args=(client,))
        thread.start()
        

receive()