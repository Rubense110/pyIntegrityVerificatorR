from logging import exception
import socket
import hmac
import hashlib
import secrets
import os
import pickle

import conf




class Generador():

    def __init__(self, host, port,msg,clave):
        self.host = host                                                                                 # Host
        self.port = port                                                                                 # Puerto
        self.msg = msg                                                                                   # Mensaje a mandar
        self.clave = clave                                                                               # Clave simetrica de cifrado
        self.nonce = secrets.token_urlsafe()                                                             # Nonce unico del mensaje
        self.msg_hmac = hmac.new(clave.encode(),(msg+self.nonce).encode(), hashlib.sha256).hexdigest()   # Resumen MAC del (mensaje+nonce) + clave simetrica
        self.nonces = []
        self.loadNonces()


    # Conexion al servidor
    def connect(self):
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            tcp_client.connect((host_ip, server_port))
        except:
            print("Servidor inalcanzable")
            exit(0)
        tcp_client.sendall(self.data.encode())
        self.received = tcp_client.recv(1024)
        tcp_client.close()

        print ("\nBytes Enviados:     {}".format(self.data)+ "\nBytes Recibidos: {}".format(self.received.decode()))
        cond = self.proof()
        if cond==0:
            print("Integridad correcta")
        elif cond==1:
            print("Incidencia de tipo 'Reply' detectada")
        else:
            print("Incidencia de tipo 'Integridad' detectada")
        
        with open(conf.NONCE_CLNT,"wb") as f:
            pickle.dump(self.nonces,f)
            f.close()


    def loadNonces(self):
        if os.path.exists(conf.NONCE_CLNT):
            with open(conf.NONCE_CLNT,"rb") as f:
                self.nonces = pickle.load(f)

    def proof(self) -> int:
        msg, nonce, hash_old = self.received.decode().split("|")
        hash_new =  hmac.new(self.clave.encode(),(msg+nonce).encode(), hashlib.sha256).hexdigest()

        if nonce not in self.nonces:
            self.nonces.append(nonce)
            if hash_old==hash_new: res = 0
            else: res = 2
        else: res = 1
        return res

    # Metodo para envio normal       
    def send(self):
        self.data = "|".join([msg,self.nonce,self.msg_hmac])
        self.connect()
    # Metodo para ataque de MitM
    def mitM(self,newmsg):
        self.data = "|".join([newmsg,self.nonce,self.msg_hmac])
        self.connect()
    # Metodo para ataque de reply
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

    a1 = Generador(host_ip,server_port,msg,key)            # mensaje normal, realmente no es ningun ataque
    a2 = Generador(host_ip,server_port,msg,key)
    a3 = Generador(host_ip,server_port,msg,key)

    #print(a1.nonce, a2.nonce, a3.nonce)
    #print(a1.msg_hmac,a2.msg_hmac,a3.msg_hmac)

    a1.send()                                       # mensaje normal, realmente no es ningun ataque
    a2.mitM(msg2)                                   # ataque MitM
    a3.replay(4)                                    # ataque Replays