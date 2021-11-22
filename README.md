___
### Project description:
In our project we have implemented a Secure peer-to-peer chatroom messaging application.
This project encrypts messages that are sent to users such that no 
message can be intersepted and decrypted. Encryption happens first 
at the client side, where the message is first encrypted with the server's 
public key. The server decryptes the message then encryptes the message again 
with the proper public key for a perticular user and routes it to, once again,
be decrypted client side. This process is repeated for every user in the chatroom.

User information such as passwords are hashed using SHA256 to ensure security 
and are stored within a password protected Database. 

This project's gui was constructed using Pyqt5 and should enable end users 
to create accounts, log into a server via hostname and port, and participate 
in chat dialogues. 
___

# Required libraries

pip install -r requirements.txt

___

# Instructions For use
___
1. The program is launched by running `%python3 client-gui.py`
   
2. log into an ilab machine (preferably) and transfer the file `cs419server2.py` and 
   `rsa2.py` and `mongo.py` and run command `%python3 cs419server2.py`
3. If you are using the service for the first time, click the "create new user" button and 
enter a username and password. 
   - Note: if the username already exists within the database
   then you must create a new account. This will direct you to the server info page and save your information
   in the database automatically, and securely. 
   
    - If you are not using the application for the first time and already have a 
    username and password, it is stored in the database, and you should 
      enter the relevant information in the username and password fields.
      
4. Once you are logged in and authenticated enter the server host name `e.g., ilab1.cs.rutgers.edu`
and the port number `8081`. 
   - Note you must host the server yourself on whatever machine you choose, however, it should 
    not be blocked by a firewall! As such it is recommended to run it on an ilab machine. 
   
5. Once you have filled out the server info page, you may begin using the chat 
service as you would any other chat service!
   
. Click the logout or disconnect buttons to leave the service. 
   