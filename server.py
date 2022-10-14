import socketserver
import hmac
import hashlib
import time
import secrets

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
        super().__init__(request, client_address, server)
            

    def handle(self):
        
        local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

        self.nonce = secrets.token_urlsafe()
        self.data = self.request.recv(1024).strip().decode()     # Cargamos el ultimo mensaje recibido al servidor
        
        print("\n{} sent:".format(self.client_address[0]))
        verificator = Verifier(self.data, sv= True)          # Comprobamos integridad del mensaje recibido
        message = local_time +" ["+self.client_address[0]+"]"+ verificator.logData + self.data.split("|")[0]
        
        msg= verificator.msgSv

        hash_new =  hmac.new(verificator.key.encode(),(msg+self.nonce).encode(), hashlib.sha256).hexdigest() # Hacemos resumen del mensaje y nonce enviado por el servidor
        respuesta =  "|".join([msg,self.nonce,hash_new])
        self.request.sendall(respuesta.encode())    # Enviamos la respuesta del servidor
        self.log(message,True)  
        print("Server reply :",msg) 
    
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
    