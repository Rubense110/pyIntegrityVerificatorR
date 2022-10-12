from logging import exception
import socket
import hmac
import hashlib
import secrets
from ssl import ALERT_DESCRIPTION_UNKNOWN_CA


key= "123456"
host_ip, server_port = "127.0.0.1", 9999
msg = "16272727 17172772 20000"

class Ataque():

    clave = key
    nonce = secrets.token_urlsafe()

    def __init__(self, host, port,msg,newmsg= None,replays= 1):
        self.host = host
        self.port = port
        self.msg_hmac = hmac.new(key.encode(),msg.encode(), hashlib.sha256).hexdigest()

        if(newmsg!= None): self.data = "|".join([newmsg,self.nonce,self.msg_hmac])
        else :             self.data = "|".join([msg,self.nonce,self.msg_hmac])

        i=0
        while(i<replays):
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
            i+=1
        


msg2= "16272728 17172772 2000000"


a1= Ataque(host_ip,server_port,msg)             # mensaje normal, realmente no es ningun ataque

a2= Ataque(host_ip,server_port,msg,msg2)       # mensaje alterado por msg2, ataque MitM

a3= Ataque(host_ip,server_port,msg,replays=4)  # mensaje repetido x veces, ataque replay
