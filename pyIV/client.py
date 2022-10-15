import socket
import hmac
import hashlib
import secrets

from verifier import Verifier

class Handler_TCPClient():
    """
    TCP Client class.
    """
    def __init__(self, host, port, msg, key):
        self.host = host                                                                                 
        self.port = port                                                                                 
        self.msg = msg                                                                                  
        self.key = key                                                                                   
        self.nonce = secrets.token_urlsafe()                                                             
        self.msg_hmac = hmac.new(key.encode(),(msg+self.nonce).encode(), hashlib.sha256).hexdigest()

    def connect(self):    # Server connection
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            tcp_client.connect((self.host, self.port))
        except:
            print("Unreachable server..")
            exit(0)

        tcp_client.sendall(self.data.encode())
        self.received = tcp_client.recv(1024)
        tcp_client.close()

        print ("\nBytes Sent:       {}".format(self.data)+ "\nBytes Received:   {}".format(self.received.decode()))
        print ("Server Response: ", self.received.decode().split("|")[0])
        Verifier(self.received.decode())

    def send(self):    # Normal message
        self.data = "|".join([self.msg,self.nonce,self.msg_hmac])
        self.connect()
    
    def mitm(self,newmsg):    # MitM attack
        self.data = "|".join([newmsg,self.nonce,self.msg_hmac])
        self.connect()
    
    def replay(self,replays):    # Replay attack
        self.data = "|".join([self.msg,self.nonce,self.msg_hmac])
        i=0
        while(i<replays):
            self.connect()
            i+=1


    




