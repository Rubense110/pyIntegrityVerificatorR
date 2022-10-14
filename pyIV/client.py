import socket
import hmac
import hashlib
import secrets

from verifier import Verifier

class Generator():

    def __init__(self, host, port,msg,clave):
        self.host = host                                                                                 # Host
        self.port = port                                                                                 # Puerto
        self.msg = msg                                                                                   # Mensaje a mandar
        self.clave = clave                                                                               # Clave simetrica de cifrado
        self.nonce = secrets.token_urlsafe()                                                             # Nonce unico del mensaje
        self.msg_hmac = hmac.new(clave.encode(),(msg+self.nonce).encode(), hashlib.sha256).hexdigest()   # Resumen MAC del (mensaje+nonce) + clave simetrica

    def connect(self):    # Conexion al servidor
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

           
    def send(self):
        self.data = "|".join([msg,self.nonce,self.msg_hmac])
        self.connect()
    
    def mitM(self,newmsg):     
        self.data = "|".join([newmsg,self.nonce,self.msg_hmac])
        self.connect()
    
    def replay(self,replays):   
        self.data = "|".join([msg,self.nonce,self.msg_hmac])
        i=0
        while(i<replays):
            self.connect()
            i+=1

if __name__ == "__main__":
    key= "123456"
    host_ip, server_port = "127.0.0.1", 9999
    msg = "16272727 17172772 20000"
    msg2= "16272728 17172772 2000000"

    a1 = Generator(host_ip,server_port,msg,key)            
    a2 = Generator(host_ip,server_port,msg,key)
    a3 = Generator(host_ip,server_port,msg,key) 

    a1.send()                                       # mensaje normal, realmente no es ningun ataque
    a2.mitM(msg2)                                   # ataque MitM
    a3.replay(4)                                    # ataque Replays