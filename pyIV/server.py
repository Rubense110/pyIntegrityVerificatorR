from distutils.core import setup
import socketserver
import hmac
import hashlib
import time
import pickle
import os

import conf

clave = "123456"

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    Clase servidor TCP.

    Nota:   Esta clase hereda de la clase 'socketserver.BaseRequestHandler'
            Implementamos el metodo handle para intercambiar datos con el
            cliente.

    """
    key = clave
    nonces = []
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        try: 
            self.loadNonces()
        finally:
            with open(conf.NONCE_SERV,"wb") as f:
                pickle.dump(self.nonces,f)
                f.close()



    def handle(self):
        
        local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

        #Cargamos el ultimo mensaje recibido al servidor
        self.data = self.request.recv(1024).strip().decode()
        #Comprobamos integridad del mensaje recibido
        cond = self.proof()
        print("{} sent:".format(self.client_address[0]))
        message = local_time +" ["+self.client_address[0]+"]"+ " [notice] " + cond[3]

        if cond[0]==0:
            message = local_time +" ["+self.client_address[0]+"]"+ " [notice] " + cond[3] 
            print("Integridad correcta\n",self.data)

            # Devolvemos el ACK al cliente, confirmando el la llegada del mensaje
            self.request.sendall("ACK from TCP Server".encode())                            

        elif cond[0]==1: 
            message = local_time +" ["+self.client_address[0]+"]"+ " [rp_error] " + cond[3]
            print("Fallo replay\n",self.data)
            self.request.sendall("Rechazado, Replay detectado".encode())

        else:
            message = local_time +" ["+self.client_address[0]+"]"+ " [int_error] " + cond[3]
            print("Fallo integridad: %s != %s " %(cond[1], cond[2]))
            self.request.sendall("Rechazado, MitM detectado".encode())

        self.log(message,True)   
        
    def loadNonces(self):
        if os.path.exists(conf.NONCE_SERV):
            with open(conf.NONCE_SERV,"rb") as f:
                self.nonces = pickle.load(f)

    def proof(self) -> tuple:
        msg, nonce, hash_old = self.data.split("|")
        hash_new =  hmac.new(self.key.encode(),(msg+nonce).encode(), hashlib.sha256).hexdigest()

        if nonce not in self.nonces:
            self.nonces.append(nonce)
            if hash_old==hash_new: res = (0, hash_old, hash_new, msg)
            else: res = (2, hash_old, hash_new, msg)
        else: res = (1, hash_old, hash_new, msg)
        return res

    def log(self,mensaje,display=False):
        """
        Devuelve por consola y escribe el log en el log file.
        """
        if display:
            print(mensaje)
        with open(conf.LOGS, 'a') as f:
            f.write("\n"+mensaje)
            f.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    #  Instanciamos el servidor TCP, aplicando el socket correspondiente (ip,puerto)
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activamos el servidor TCP.
    # Para abortar el servidor presionar Ctrl-C
    try:
        print("Servidor activo (HOST: %s ,PORT: %d)\n" %(HOST, PORT)) 
        tcp_server.serve_forever()

    except Exception as e:
        print("Error de apertura servidor: ",e)
    