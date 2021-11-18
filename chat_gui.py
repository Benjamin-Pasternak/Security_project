import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class Login(QDialog):
    
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        
        #self.titleLabel.adjustSize()
        
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)     # Changes password visability
        self.loginButton.clicked.connect(self.login)
        self.createAccountButton.clicked.connect(self.goToCreateAccount) 
    
    
    def login(self):
        '''
            [Called on loginButton press]
        *Handles user login
        *redirects to home frame when succesful
        '''
        username = self.username.text()
        password = self.password.text()
        
        print(f"{username}:{password}")
        
        
        """
        VALIDATE USER DATA, IF LOGIN SUCCESFUL TRANSTION TO MAIN CHAT WINDOW
        """
       
        self.goToServerInfo()

        
        ''' Frame Transition Functions''' 
        
    def goToCreateAccount(self):
        '''
            [Called on createAccountButton press]
        Redirects user to the account creation frame    
        '''
        
        createAccountWindow = CreateAccount()
        widget.addWidget(createAccountWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
        
    def goToServerInfo(self):
        serverInfo = JoinServer()
        widget.addWidget(serverInfo)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
        
    def goToChatWindow(self):
        
        chatWindow = ChatWindow()
        widget.addWidget(chatWindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedWidth(720)
        widget.setFixedHeight(620)    

        
class CreateAccount(QDialog):
    
    def __init__(self):
        
        super(CreateAccount, self).__init__()
        loadUi("createAccount.ui", self)
        
        self.signupButton.clicked.connect(self.createAccount)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmPassword.setEchoMode(QtWidgets.QLineEdit.Password)


    def createAccount(self):
        '''
            [Called on signupButton press]
            
            Collects new user data and validates passwords
            *Adds new user to database 
            Redirects new user to the login page after account creation
        
        '''

        username = self.username.text()

        if self.password.text()==self.confirmPassword.text():
            password=self.password.text()
                        
            print(f"Successfully created account({username}:{password})... ")
            
            """
            ADD USER INFORMATION TO DATABASE
            """
            
            login=Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)



class ChatWindow(QDialog):
    
    def __init__(self):
        
        super(ChatWindow, self).__init__()
        loadUi("chat_window.ui", self)

        self.sendButton.clicked.connect(self.sendMessage)
        self.disconnectButton.clicked.connect(self.disconnectFromServer)


    def sendMessage(self):
        
        msg = self.userInput.text()
        self.userInput.clear()      # Clear previous msg
        
        if len(msg) > 0:
            print(msg)
            
            self.chatLog.append(f"User:{msg}")      # Add user msg to chat window
        
        """
        Encrypt msg and send over socket
        """


    def disconnectFromServer(self):
        
        
        ''' Redirect back to join server page'''
        joinServer = JoinServer()
        widget.addWidget(joinServer)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
        

    



class JoinServer(QDialog):
    
    def __init__(self):
        
        super(JoinServer, self).__init__()
        loadUi("serverInfo.ui", self)

        self.connectButton.clicked.connect(self.connectToServer)

        
    def connectToServer(self):
        
        ip = self.server.text()
        port = self.port.text()
        connected = True
            
        if connected:
            self.chatLog.append(f"[SERVER]: Successfully connected to ({ip} : {port})")
            
        else:
            self.chatLog.append(f"[SERVER]: Failed to connect to ({ip} : {port})")


  
        








app=QApplication(sys.argv)
mainwindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec_()