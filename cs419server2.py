import socket
import threading
from threading import Thread
from threading import Event
import ast
import rsa2
import mongo

# Host Machine Ip
hostname = socket.gethostname()
host = socket.gethostbyname(hostname)

# unreserved port
port = 8081
#mongs
mongodb_atlas_test = mongo.mongodb_atlas_test()
print(f"Host: {hostname} @ {host}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(2)

# lists of clients accessing server and current usernames
clientList = []
usernameList = []
#thread = threading.Thread

def send_message(message, usernamesend):
    print(message)
    for client in clientList:
        username = usernameList[clientList.index(client)]
        print(username)
        encoded = int.from_bytes(bytes(message, 'utf-8'), 'big')
        temp = mongodb_atlas_test.get_data(username)
        print(temp[0]['publicKey'])
        key = temp[0]['publicKey']
        key = key.replace('(', '')
        key = key.replace(')', '')
        n = int(key.partition(', ')[0])
        e = int(key.partition(', ')[2])
        print(n)
        print(e)
        c = rsa2.rsa_encrypt_message(encoded, e, n)
        c = str(c)
        print(c)
        msg = f"{usernamesend.upper()}: {c}"
        print(msg)
        client.send(msg.encode("utf-8"))

def send_greeting(message):
    for client in clientList:
        client.send(message.encode("utf-8"))

# client handler: receive and send client messages and check if they left. If left, then remove from lists
def client_handler(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            username= message.partition(': ')[0]
            encoded = message.partition(': ')[2]
            #username = message.partition(': ')[0]
            # # print(type(encoded))
            encoded = ast.literal_eval(encoded)
            print(type(encoded))
            print(encoded)
            d = 77662288554955611269468421722416415173589480086644379349629325316263250775289168432059285971035963588531522191335016219514518397293345441637556097021190196590067231699963372870059580959039385862219396355823627733372975069319803081851604979459033096929149989819950906810573669317842769071454286589443669283587
            n = 116493432832433416904202632583624622760384220129966569024443987974394876162933752648088928956553945382797283287002524329271777595940018162456334145531785316822475007069649551189505369551771432965666304285638711211771988376956218991950664736131801653454935687886869449163747435305275635711504309569103013484449
            print(n)
            print(d)
            # # n, e = self.public_key_format(temp[0]['publicKey'])
            # # m2 = int(''.join())
            c = rsa2.rsa_decrypt_message(encoded, d, n)
            #
            print("here", c)
            c = int(''.join([str(x) for x in c]))
            # # c = c.to_bytes((c.bit_length()+7)//8,'big')
            c = c.to_bytes((c.bit_length() + 7) // 8, 'big').decode('utf-8')
            print(c)
            send_message(c, username)
        except:
            clientIndex = clientList.index(client)
            clientList.remove(client)
            client.close()
            username = usernameList[clientIndex]
            send_greeting('{} left'.format(username))
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

        send_greeting("New user {} joined".format(username))
        client.send('You have connected to server'.encode('utf-8'))
        print("ready")
        # usernameList2 = 'USERLIST' + str(usernameList)
        #
        # # print(usernameList2)
        # # print(len(usernameList2))
        # # for client in clientList:
        # #     client.send(usernameList2.encode('utf-8'))
        # send_message(usernameList2.encode('utf-8'))
        thread = threading.Thread(target=client_handler, args=(client,))
        thread.start()
        # recv_thread = ReceiveThread(client, Stop)
        # recv_thread.start()
        # print("bout to join")
        # recv_thread.join()
        # print("joined")
# class ReceiveThread(Thread):
#
#
#     def __init__(self,client, stop):
#         Thread.__init__(self)
#         self.StopEvent = stop
#         self.client = client
#
#     def run(self):
#         while True:
#             client_handler(self.client)
#             if (self.StopEvent.wait(0)):
#                 print("Asked to stop")
#                 break;


Stop = Event()
receive()