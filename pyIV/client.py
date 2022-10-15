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
            tcp_client.connect((host_ip, server_port))
        except:
            print("Unreachable Server")
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

if __name__ == "__main__":
    key= "123456"
    host_ip, server_port = "127.0.0.1", 9999
    msg = "16272727 17172772 20000"
    msg2= "16272728 17172772 2000000"

    a1 = Handler_TCPClient(host_ip,server_port,msg,key)            
    a2 = Handler_TCPClient(host_ip,server_port,msg,key)
    a3 = Handler_TCPClient(host_ip,server_port,msg,key) 

    a1.send()                                       # Message 
    a2.mitm(msg2)                                   # MitM attack
    a3.replay(4)                                    # Replay attack