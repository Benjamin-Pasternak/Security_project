import socket
import threading
from threading import Thread
from threading import Event

# Host Machine Ip
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)

# unreserved port
port = 8081

print(f"Host: {hostname} @ {host}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

# lists of clients accessing server and current usernames
clientList = []
usernameList = []
thread = threading.Thread

def send_message(message):
    for client in clientList:
        client.send(message)


# client handler: receive and send client messages and check if they left. If left, then remove from lists
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
            Stop.set()
            break


# receive clients, enter into clientList and usernameList
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

        # TODO give each user unique id, probably set id to a counter

        send_message("New user {} joined".format(username).encode('utf-8'))
        # client.send('You have connected to server'.encode('utf-8'))
        usernameList2 = 'USERLIST' + str(usernameList)

        # print(usernameList2)
        # print(len(usernameList2))
        # for client in clientList:
        #     client.send(usernameList2.encode('utf-8'))
        send_message(usernameList2.encode('utf-8'))
        recv_thread = ReceiveThread(client, Stop)
        recv_thread.start()
        print("bout to join")
        recv_thread.join()
        print("joined")
class ReceiveThread(Thread):


    def __init__(self,client, stop):
        Thread.__init__(self)
        self.StopEvent = stop
        self.client = client

    def run(self):
        while True:
            client_handler(self.client)
            if (self.StopEvent.wait(0)):
                print("Asked to stop")
                break;


Stop = Event()
receive()