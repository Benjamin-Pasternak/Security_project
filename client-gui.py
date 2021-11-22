import sys
import socket
import threading
import pymongo
import mongo
import rsa2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt

import ast


class Client(object):

    def __init__(self):

        self.username = ''
        self.first = 1
        self.activeusers = []
        # mongodb_atlas_test = mongodb_atlas_test()
        ''' Setup Join Server Window '''
        self.joinServer = JoinServer()
        # self.joinServer.show()
        self.joinServer.setHidden(True)
        self.joinServer.setFixedWidth(420)
        self.joinServer.setFixedHeight(500)
        self.joinServer.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        ''' Join Server Window Buttons'''
        self.joinServer.logoutButton.clicked.connect(self.logout2)
        self.joinServer.connectButton.clicked.connect(self.connectToServer)

        ''' Setup Login Window '''
        self.loginUI = Login()
        self.loginUI.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.loginUI.setHidden(True)
        self.loginUI.show()
        self.loginUI.setFixedHeight(500)
        self.loginUI.setFixedWidth(420)
        self.loginUI.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginUI.loginButton.clicked.connect(self.login)
        self.loginUI.createAccountButton.clicked.connect(self.movetocreate)

        ''' Setup Account Creation '''
        self.createAcc = CreateAccount()
        self.createAcc.setHidden(True)
        # self.createAcc.show()
        self.createAcc.setFixedHeight(500)
        self.createAcc.setFixedWidth(470)
        self.createAcc.confirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.createAcc.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.createAcc.signupButton.clicked.connect(self.create)

        ''' Setup Chat Window '''
        self.chatWindow = ChatWindow()
        self.chatWindow.setHidden(True)
        self.chatWindow.setFixedHeight(645)
        self.chatWindow.setFixedWidth(880)
        self.chatWindow.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.chatWindow.sendButton.clicked.connect(self.send_message)
        self.chatWindow.disconnectButton_2.clicked.connect(self.logout)
        self.chatWindow.disconnectButton.clicked.connect(self.disconnect)

        ''' Create Client socket'''
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ''' User list dynamic'''
        self.userList = ''

    '''             Client Functions
    ==============================================================='''

    ''' Handles client connection and setup
        Uses connect() helper to manage client connection
        Manages frame transition
        Starts thread for receiving messages
    '''

    def connectToServer(self):
        host = self.joinServer.server.text()
        port = self.joinServer.port.text()

        #print(f"{host}:{port}")

        if self.connect(host, int(port)):
            self.joinServer.setHidden(True)
            self.chatWindow.setVisible(True)
            #self.receive_message()
            self.recv_thread = ReceiveThread(self.clientSocket)
            self.recv_thread.signal.connect(self.show_message)
            self.recv_thread.start()
            #print("[CLIENT]: Recv thread started...")

    
    def login(self):
        '''
            [Called on loginButton press]
        *Handles user login
        *redirects to home frame when succesful
        '''
        username = self.loginUI.username.text()
        self.username = self.loginUI.username.text()
        password = self.loginUI.password.text()  # unsafe hash it immediatly when you input it
        the = mongodb_atlas_test.get_data(username)
        #print(type(the))
        # checking if the password is
        if the:
            passtemp = the[0]['password']
        else:
            passtemp = "no"
        
        password = rsa2.hash_password(password)
        # passtemp = rsa2.hash_password(passtemp)
        #print(f"{username}: {password}")

        """
        VALIDATE USER DATA, IF LOGIN SUCCESFUL TRANSTION TO MAIN CHAT WINDOW
        """

        if password == passtemp:
            # print('PASSED!')
            self.loginUI.setHidden(True)
            self.joinServer.setVisible(True)
        else:
            self.show_error('Login Error', 'Wrong Username or Password')

    def movetocreate(self):
        '''
            change to create account ui
        '''
        self.loginUI.setHidden(True)
        self.createAcc.setVisible(True)

    def create(self):
        '''
            create new account and automatically login
        '''
        username = self.createAcc.username.text()
        password = self.createAcc.password.text()
        confPass = self.createAcc.confirmPassword.text()
        # print("[us]:", username)
        # print("[pass]:", password)
        # print("[conf]:", confPass)
        the = mongodb_atlas_test.get_data(username)
        # temp = str(the[0])
        # num = temp.find('username')
        # num = num + 12
        # temp = temp[num:]
        # num2 = temp.find("'")
        # usetemp = temp[:num2]
        if not the:  # if the database does not contain the record
            if confPass == password:  # if passwords match
                self.username = username
                public_key, private_key = rsa2.gen_keys()
                # print("e",e)
                # print("pub key:", public_key)
                # print("n?",public_key[0] )
                # private_key = rsa2.gen_private_key(public_key[0], e)
                #print("d", private_key[1] )
                public_key = str(public_key)
                private_key = str(private_key)
                # print(public_key)
                # print(private_key)
                data2 = {
                    "username": username,
                    "password": rsa2.hash_password(password),
                    "publicKey": public_key
                }
                #data3  = username +
                # json_write = json.dumps({'username': username, 'private_key': private_key})
                with open('secretstuff.txt', 'a') as f:
                    f.write(username + ": ")
                    f.write(str(private_key)+'\n')
                mongodb_atlas_test.insert_data(data2)
                self.createAcc.setHidden(True)
                self.joinServer.setVisible(True)

            else:
                self.show_error('Account Creation Error', 'Passwords do not match')
        else:
            self.show_error('Account Creation Error', 'Username taken')

    def logout(self):
        '''
            [Called on logout press]
        *Handles user logout
        *redirects to home frame when succesful
        '''
        self.username = ''
        self.first = 1
        # self.recv_thread.end()
        self.clientSocket.close()
        self.chatWindow.setHidden(True)
        self.loginUI.setVisible(True)
        self.loginUI.username.clear()
        self.loginUI.password.clear()
        self.chatWindow.chatLog.clear()
        self.joinServer.server.clear()
        self.joinServer.port.clear()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def logout2(self):
        '''
            [Called on logout press]
        *Handles user logout
        *redirects to home frame when succesful
        '''
        self.username = ''
        self.first = 1
        # self.recv_thread.end()
        self.clientSocket.close()
        self.joinServer.setHidden(True)
        self.loginUI.setVisible(True)
        self.loginUI.username.clear()
        self.loginUI.password.clear()
        self.chatWindow.chatLog.clear()
        self.joinServer.server.clear()
        self.joinServer.port.clear()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def disconnect(self):
        '''
            [Called on disconnectButton press]
        *Handles user disconnecting from server
        *redirects to home frame when succesful
        '''
        #self.username = ''
        # self.recv_thread.end()
        self.first = 1
        self.clientSocket.close()
        self.chatWindow.setHidden(True)
        self.joinServer.setVisible(True)
        self.chatWindow.chatLog.clear()
        self.joinServer.server.clear()
        self.joinServer.port.clear()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def show_message(self, message):
        #print("Mes: :",message)
        if message == 'USERNAME':

            self.send_message()
        elif message == 'You have connected to server':
            self.chatWindow.chatLog.append("You have connected to server")
            #self.send_message()
        elif "New user" in message and "joined the chat" in message:
            # print("butwhy")
            self.chatWindow.chatLog.append(message)
        elif 'USERLIST' in message:

            userlist = message.replace('You have connected to server', '')
            userlist = userlist.replace('USERLIST', '')

            userlist = userlist.replace(',', '')
            userlist = userlist.replace('[', '')
            userlist = userlist.replace(']', '')
            userlist = userlist.replace("'", '')
            #print(userlist)
            users = userlist.strip()
            self.activeusers = users.split(' ')

            userlist = userlist.replace(self.username.upper(), '')
            userlist = userlist.strip()

            self.userList = userlist

            self.chatWindow.activeUsers.setPlainText('\n'.join(self.activeusers))

        elif "User" in message and "left the chat" in message:
            #print("butwhy")
            self.chatWindow.chatLog.append(message)
            user = message.replace(' left the chat', '')
            user = user.replace('User ', '')
            #print(user)
            #print(self.activeusers)
            self.activeusers.remove(user)
            self.chatWindow.activeUsers.setPlainText('\n'.join(self.activeusers))

        else:
            #encoded = int.from_bytes(bytes(message, 'utf-8'), 'big')
            # userlist is now empty
            user = message.partition(': ')[0]
            #print(user)
            encoded = message.partition(': ')[2]
           # print(type(encoded))
            encoded = ast.literal_eval(encoded)
            #print(type(encoded))
            #print(encoded)
            key = self.get_privateKey(self.username)
            key = key.replace('(', '')
            key = key.replace(')', '')
            n = int(key.partition(', ')[0])
            #print(n)
            #d = int(key[key.index(', ') + 2:-1])
            d = int(key.partition(', ')[2])
            #print(d)
            #n, e = self.public_key_format(temp[0]['publicKey'])
            #m2 = int(''.join())
            c = rsa2.rsa_decrypt_message(encoded, d, n)


            #print("here",c)
            c = int(''.join([str(x) for x in c]))
            #c = c.to_bytes((c.bit_length()+7)//8,'big')
            c = c.to_bytes((c.bit_length() + 7) // 8, 'big').decode('utf-8')
            #print(c)
            msg = f"{user.upper()}: {c}"
            self.chatWindow.chatLog.append(msg)

    ''' Connect client to server'''

    def connect(self, host, port):

        try:
            self.clientSocket.connect((host, int(port)))
            #print(f"[CLIENT]: Connected to server {host}:{port}...")
            return True
        except Exception as e:
            error_msg = f"Error while trying to connect to server...\n{str(e)}\n Please re-enter server information... "
            #print("[CLIENT]:", error_msg)
            self.show_error("Server Error", error_msg)
            self.joinServer.server.clear()
            self.joinServer.port.clear()

            return False

    def get_privateKey(self, username):
        try:
            with open('./secretstuff.txt') as file:
                text = file.readlines()
            index = 0
            for line in text:
                #print(line)
                if username in line:
                    #print(line)
                   #print(text[]1)
                    key = line
                    key = key.partition(': ')[2]
                    #print("key:",key)
                    key = key.replace('(', '')
                    key = key.replace(')', '')
                    #print(key)
                    #return int(key[1:key.index(', ')]), int(key[key.index(', ') + 2:-1])
                    return str(key)
                #print("OW")
        except:
            print('error no secret keys stored')

    def public_key_format(self, key):
        key = key.replace('(', '')
        key = key.replace(')', '')
        n = int(key.partition(', ')[0])
        e = int(key.partition(', ')[2])
        return n, e

    def send_message(self):
        msg = self.chatWindow.userInput.text()
        if self.first == 1:
            msg = f"{self.username.upper()}: {msg}"
            self.clientSocket.send(msg.encode('utf-8'))
            self.first = 0
        else:
            try:
                # if self.userList.replace(' ', '') != '':
                #     encoded = int.from_bytes(bytes(msg, 'utf-8'), 'big')
                #     # userlist is now empty
                #     temp = mongodb_atlas_test.get_data(self.userList)
                #     print(temp[0]['publicKey'])
                #     n, e = self.public_key_format(temp[0]['publicKey'])
                #
                #     c = rsa2.rsa_encrypt_message(encoded, e, n)
                #     c = str(c)
                #
                #     print(self.userList)
                #     msg = f"{self.username.upper()}: {c}"
                #     self.clientSocket.send(msg.encode('utf-8'))
                #     self.chatWindow.userInput.clear()
                # else:
                 encoded = int.from_bytes(bytes(msg, 'utf-8'), 'big')
                 # userlist is now empty
                 # temp = mongodb_atlas_test.get_data(self.username)
                 # print(temp[0]['publicKey'])
                 # n, e = self.public_key_format(temp[0]['publicKey'])
                 n = 116493432832433416904202632583624622760384220129966569024443987974394876162933752648088928956553945382797283287002524329271777595940018162456334145531785316822475007069649551189505369551771432965666304285638711211771988376956218991950664736131801653454935687886869449163747435305275635711504309569103013484449
                 e = 3
                 #print(n)
                 #print(e)
                 c = rsa2.rsa_encrypt_message(encoded, e, n)
                 c = str(c)
                 #print(c)
                 msg = f"{self.username.upper()}: {c}"
                 self.clientSocket.send(msg.encode('utf-8'))
                 self.chatWindow.userInput.clear()
            except Exception as e:
                print('EXCEPT', self.userList)
                error_msg = f"Error while trying to send message...\n{str(e)}"
                print("[CLIENT]:", error_msg)
                self.show_error("Server Error", error_msg)

    ''' Creates a message box to display error messages'''

    def show_error(self, error_type, message):
        errorDialog = QtWidgets.QMessageBox()
        errorDialog.setText(message)
        errorDialog.setWindowTitle(error_type)
        errorDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
        errorDialog.exec_()


''' Class to handle receiving messages from thread using pyqt signals'''


class ReceiveThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)

    def __init__(self, client_socket):
        super(ReceiveThread, self).__init__()
        self.client_socket = client_socket

    def run(self):
        while True:
            self.receive_message()

    def receive_message(self):

        while True:
            try:
                message = self.client_socket.recv(1024)


                message = message.decode()

                #print(message)
                self.signal.emit(message)
            except:
                break


''' GUI frame classes'''


class JoinServer(QDialog):

    def __init__(self):
        super(JoinServer, self).__init__()
        loadUi("serverInfo.ui", self)

        # self.connectButton.clicked.connect(self.connectToServer)


class ChatWindow(QDialog):

    def __init__(self):
        super(ChatWindow, self).__init__()
        loadUi("chat_window.ui", self)


class CreateAccount(QDialog):

    def __init__(self):
        super(CreateAccount, self).__init__()
        loadUi("createAccount.ui", self)


class Login(QDialog):

    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)  # Changes password visability


if __name__ == "__main__":
    mongodb_atlas_test = mongo.mongodb_atlas_test()

    ''' Fixes High Resolution Display Scaling Bug '''
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
