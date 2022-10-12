from logging import exception
import socket
import hmac
import hashlib
import secrets


key= "123456"
host_ip, server_port = "127.0.0.1", 9999
msg = "16272727 17172772 20000"
msg2= "16272728 17172772 2000000"

class Generador():

    clave = key
    

    def __init__(self, host, port,msg):
        self.host = host
        self.port = port
        self.msg_hmac = hmac.new(key.encode(),msg.encode(), hashlib.sha256).hexdigest()
        self.nonce = secrets.token_urlsafe()

    def connect(self):
            tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                tcp_client.connect((host_ip, server_port))
            except:
                print("Servidor inalcanzable")
                exit(0)
            tcp_client.sendall(self.data.encode())
            received = tcp_client.recv(1024)
            tcp_client.close()
            print ("Bytes Enviados:     {}".format(self.data)+ "\nBytes Recibidos: {}".format(received.decode()))
            
    def send(self):
        self.data = "|".join([msg,self.nonce,self.msg_hmac])
        self.connect()

    def MitM(self,newmsg):
        self.data = "|".join([newmsg,self.nonce,self.msg_hmac])
        self.connect()

    def Replay(self,replays):
        self.data = "|".join([msg,self.nonce,self.msg_hmac])
        i=0
        while(i<replays):
            self.connect()
            i+=1

        





a1=  Generador(host_ip,server_port,msg)            # mensaje normal, realmente no es ningun ataque
a2 = Generador(host_ip,server_port,msg)
a3 = Generador(host_ip,server_port,msg)

#print(a1.nonce, a2.nonce, a3.nonce)
#print(a1.msg_hmac,a2.msg_hmac,a3.msg_hmac)

a1.send()                                       # mensaje normal, realmente no es ningun ataque
a2.MitM(msg2)                                   # ataque MitM
a3.Replay(4)                                    # ataque Replays