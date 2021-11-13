import sys
import socket
import threading
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi







class Client(object):
    
    def __init__(self):
        
        self.username = ''
        
        ''' Setup Join Server Window '''
        self.joinServer = JoinServer()
        self.joinServer.show()
        self.joinServer.setFixedWidth(480)
        self.joinServer.setFixedHeight(620)
        
        ''' Join Server Window Buttons'''
        self.joinServer.connectButton.clicked.connect(self.connectToServer)
        
        
        
        ''' Setup Login Window '''
        self.loginUI = Login()
        self.loginUI.setHidden(True)
        #self.loginUI.show()
        self.loginUI.setFixedHeight(620)
        self.loginUI.setFixedWidth(480)
        
        ''' Setup Chat Window '''
        self.chatWindow = ChatWindow()
        self.chatWindow.setHidden(True)
        self.chatWindow.sendButton.clicked.connect(self.send_message)
        
        
        
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
        
        if self.connect(host,int(port)):
            
            self.joinServer.setHidden(True)
            self.chatWindow.setVisible(True)
            
            
            
            self.recv_thread = ReceiveThread(self.clientSocket)
            self.recv_thread.signal.connect(self.show_message)
            self.recv_thread.start()
            print("[CLIENT]: Recv thread started...")
        
            
            
       
    ''' Display received message in chat log '''    
    def show_message(self, message):
        if message == 'USERNAME':
            self.chatWindow.chatLog.append("Please enter your username...")
        else:
            self.chatWindow.chatLog.append(message)
        
        
    ''' Connect client to server'''    
    def connect(self,host, port):
        
        try:
            self.clientSocket.connect((host,int(port)))
            print(f"[CLIENT]: Connected to server {host}:{port}...")
            return True
        except Exception as e:
            error_msg = f"Error while trying to connect to server...\n{str(e)}\n Please re-enter server information... "
            print("[CLIENT]:", error_msg)
            self.show_error("Server Error", error_msg)
            self.joinServer.server.clear()
            self.joinServer.port.clear()
            
            return False
        
    
    ''' Send Message to client '''
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
        
        message = self.client_socket.recv(1024)
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
        
        super(ChatWindow,self).__init__()
        loadUi("chat_window.ui",self)
       
        
        
        
        
class Login(QDialog):
    
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        
    
        
      
        
        
        
    





if __name__ == "__main__":
            
    app=QtWidgets.QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())
        
        
        