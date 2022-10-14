from copyreg import pickle
import socketserver
import hmac
import hashlib
import time
import secrets
import random
import pickle

import conf
from verifier import Verifier

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    Clase servidor TCP.

    Nota:   Esta clase hereda de la clase 'socketserver.BaseRequestHandler'
            Implementamos el metodo handle para intercambiar datos con el
            cliente.

    """

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server )
        
            

    def handle(self):
        
        local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

        self.nonce = secrets.token_urlsafe()
        self.data = self.request.recv(1024).strip().decode()     # Cargamos el ultimo mensaje recibido al servidor
        
        print("\n{} sent:".format(self.client_address[0]))
        self.verificator = Verifier(self.data, sv= True)          # Comprobamos integridad del mensaje recibido
        self.message = local_time +" ["+self.client_address[0]+"]"+ self.verificator.logData + self.data.split("|")[0]
        self.msg= self.verificator.msgSv
        self.reply()
    
    def reply(self):
        attack = True
        self.msg2 = self.msg

        if attack == True:
            x = random.random()
            if(x<1/3): 
                self.msg2 = self.msg+" theMANisHERE"
            elif x>= 1/3 and x<2/3: 
                with open(conf.NONCE_CLNT, "rb") as f:
                    self.nonce = pickle.load(f)[-1]
                    f.close()
        
        hash_new =  hmac.new(self.verificator.key.encode(),(self.msg+self.nonce).encode(), hashlib.sha256).hexdigest() # Hacemos resumen del mensaje y nonce enviado por el servidor
        respuesta =  "|".join([self.msg2,self.nonce,hash_new])
        self.request.sendall(respuesta.encode())    # Enviamos la respuesta del servidor
        self.log(self.message,True)  
        print("Server response: ",self.msg2) 


    def log(self,mensaje,display=False):
        """
        Devuelve por consola y escribe el log en el log file.
        """
        if display: print(mensaje)        
        with open(conf.LOGS, 'a') as f:
            f.write("\n"+mensaje)
            f.close()

if __name__ == "__main__":

    HOST, PORT = "localhost", 9999
    handler_tcp = Handler_TCPServer  
    tcp_server = socketserver.TCPServer((HOST, PORT), handler_tcp) #  Instanciamos el servidor TCP, aplicando el socket correspondiente y nuestro handler

    try:
        print("Servidor activo (HOST: %s ,PORT: %d)\n" %(HOST, PORT))   # Activamos el servidor TCP.
        tcp_server.serve_forever()                                      # Para abortar el servidor presionar Ctrl-C

    except Exception as e:
        print("Error de apertura servidor: ",e)
    