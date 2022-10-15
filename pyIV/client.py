import socket
import hmac
import hashlib
import secrets
import os
import time

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

    print("Realizar transferencia bancaria \n")
    cuenta_org = input("Introduce cuenta origen (6 digitos) : ")
    cuenta_dest = input("Introduce cuenta destino (6 digitos) : ")
    cantidad = input("Introduce la cantidad a mandar: ")
    msg = cuenta_org+" "+cuenta_dest+" "+cantidad
    print("\n Transferencia: ", msg)
    
    print("\n Acciones a realizar: ")
    print("[1] Envío de transferencia")
    print("[2] Simulación ataque MitM")
    print("[3] Simulación ataque de Replay")
    case1 = int(input("Escoja opción: "))

    while case1 >3 or case1==0:
        case1 = int(input("Debe escoger entre [1 | 2 | 3], escoja opción: "))

    if case1 == 1:
        print("####### Realizando la transferencia... #######\n")

        a1 = Handler_TCPClient(host_ip,server_port,msg,key)
        try: 
            a1.send()
        except Exception as e:
            os.system("taskkill /f /im  server.exe")

    elif case1 == 2:
        print("####### Simulación ataque MitM #######\n")

        print("Modificar el mensage original...\n")
        print("Cuenta origen original: ",cuenta_org)
        cuenta_org1 = input("Introduce cuenta origen (6 digitos) : ")
        print("\nCuenta destino original: ",cuenta_dest)
        cuenta_dest1 = input("Introduce cuenta destino (6 digitos) : ")
        print("\nCantidad original: ", cantidad)
        cantidad1 = input("Introduce la cantidad a mandar: ")
        msg1 = cuenta_org1+" "+cuenta_dest1+" "+cantidad1
        print("\n Transferencia modificada ^_^: ", msg1)
        a2 = Handler_TCPClient(host_ip,server_port,msg,key)
        try: 
            a2.mitm(msg1)
        except Exception as e:
            os.system("taskkill /f /im  server.exe")
    else:
        print("####### Simulación ataque de Replay #######\n")
        
        reps = int(input("Introducir el numero de repeticiones del mensaje: "))
        a3 = Handler_TCPClient(host_ip,server_port,msg,key)
        try:
            a3.replay(reps)
        except Exception as e:
            os.system("taskkill /f /im  server.exe")

    




