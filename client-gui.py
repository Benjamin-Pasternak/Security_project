import sys
import socket
import threading
import pymongo
import mongo
import rsa2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import json



class Client(object):
    
    def __init__(self):
        
        self.username = ''

       # mongodb_atlas_test = mongodb_atlas_test()
        ''' Setup Join Server Window '''
        self.joinServer = JoinServer()
       # self.joinServer.show()
        self.joinServer.setHidden(True)
        self.joinServer.setFixedWidth(480)
        self.joinServer.setFixedHeight(620)
        
        ''' Join Server Window Buttons'''
        self.joinServer.connectButton.clicked.connect(self.connectToServer)
        
        
        
        ''' Setup Login Window '''
        self.loginUI = Login()
        self.loginUI.setHidden(True)
        self.loginUI.show()
        self.loginUI.setFixedHeight(620)
        self.loginUI.setFixedWidth(480)

        self.loginUI.loginButton.clicked.connect(self.login)
        self.loginUI.createAccountButton.clicked.connect(self.movetocreate)

        ''' Setup Account Creation '''
        self.createAcc = CreateAccount()
        self.createAcc.setHidden(True)
       # self.createAcc.show()
        self.createAcc.setFixedHeight(620)
        self.createAcc.setFixedWidth(480)

        self.createAcc.signupButton.clicked.connect(self.create)

        ''' Setup Chat Window '''
        self.chatWindow = ChatWindow()
        self.chatWindow.setHidden(True)
        self.chatWindow.sendButton.clicked.connect(self.send_message)
        self.chatWindow.disconnectButton_2.clicked.connect(self.logout)
        self.chatWindow.disconnectButton.clicked.connect(self.disconnect)
        
        ''' Create Client socket'''
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



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
        
        print(f"{host}:{port}")
        
        if self.connect(host, int(port)):
            
            self.joinServer.setHidden(True)
            self.chatWindow.setVisible(True)
            
            
            
            self.recv_thread = ReceiveThread(self.clientSocket)
            self.recv_thread.signal.connect(self.show_message)
            self.recv_thread.start()
            print("[CLIENT]: Recv thread started...")

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
        # checking if the password is
        passtemp = the[0]['password']
        # temp = str(the[0])
        # # print('here', type(temp), type(the[0]))
        # num = temp.find('password')
        # num = num + 12
        # temp = temp[num:]
        # num2 = temp.find("'")
        # passtemp = temp[:num2]
        password = rsa2.hash_password(password)
        # passtemp = rsa2.hash_password(passtemp)
        print(f"{username}: {password}")


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
        #usetemp = temp[:num2]
        if not the:  # if the database does not contain the record
            if confPass == password:  # if passwords match
                self.username = username
                public_key, e = rsa2.gen_public_key()
                private_key = rsa2.gen_private_key(public_key[0], e)
                public_key = str(public_key)
                private_key = str(private_key)
                # print(public_key)
                # print(private_key)
                temppass = rsa2.hash_password(password)
                data2 = {
                    "username": username,
                    "password": temppass,
                    "publicKey": public_key
                }
                # json_write = json.dumps({'username': username, 'private_key': private_key})
                with open('secretstuff.txt', 'a') as f:
                    f.write(username + '\n')
                    f.write(str(private_key))
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
        #self.recv_thread.end()
        self.clientSocket.close()
        self.chatWindow.setHidden(True)
        self.loginUI.setVisible(True)

    def disconnect(self):
        '''
            [Called on disconnectButton press]
        *Handles user disconnecting from server
        *redirects to home frame when succesful
        '''
        self.username = ''
       # self.recv_thread.end()
        self.clientSocket.close()
        self.chatWindow.setHidden(True)
        self.joinServer.setVisible(True)

    ''' Display received message in chat log '''    
    def show_message(self, message):
        if message == 'USERNAME':
            self.chatWindow.chatLog.append("Please enter your username...")
            self.send_message()
        else:
            self.chatWindow.chatLog.append(message)
        
        
    ''' Connect client to server'''    
    def connect(self, host, port):
        
        try:
            self.clientSocket.connect((host, int(port)))
            print(f"[CLIENT]: Connected to server {host}:{port}...")
            return True
        except Exception as e:
            error_msg = f"Error while trying to connect to server...\n{str(e)}\n Please re-enter server information... "
            print("[CLIENT]:", error_msg)
            self.show_error("Server Error", error_msg)
            self.joinServer.server.clear()
            self.joinServer.port.clear()
            
            return False
        
    def get_privateKey(self):
        try:
            with open('./secretstuff.txt') as file:
                text = file.readlines()
            key = text[1]
            return int(key[1:key.index(', ')]), int(key[key.index(', ')+2:-1])
        except:
            print('error no secret keys stored')

    def public_key_format(self, key):
        return int(key[1:key.index(', ')]), int(key[key.index(', ') + 2:-1])

    def send_message(self):
        msg = self.chatWindow.userInput.text()

        if self.username == '':
            self.username = msg
        else:
            msg = f"{self.username.upper()}: {msg}"

        try:
            self.clientSocket.send(msg.encode('utf-8'))
            self.chatWindow.userInput.clear()
        except Exception as e:
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
            message = self.client_socket.recv(1024)
            if len(message) == 0:
                break
            message = message.decode()

            print(message)
            self.signal.emit(message)



''' GUI frame classes'''
        
class JoinServer(QDialog):
    
    def __init__(self):
        
        super(JoinServer,self).__init__()
        loadUi("serverInfo.ui",self)

        #self.connectButton.clicked.connect(self.connectToServer)

        
    


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
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)  # Changes password visability

        

if __name__ == "__main__":
    mongodb_atlas_test = mongo.mongodb_atlas_test()
    app=QtWidgets.QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
        
        
        