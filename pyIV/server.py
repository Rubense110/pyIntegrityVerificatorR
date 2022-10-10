import socketserver
import hmac
import hashlib
import time

import conf

def proof(data):
        key= "123456"
        hash_old = data.split("|")[1].strip()
        msg = data.split("|")[0].strip()
        hash_new = hmac.new(key.encode(),msg.encode(), hashlib.sha256).hexdigest()

        if hash_old==hash_new:
            return (True, hash_old, hash_new, msg)

        return (False, hash_old, hash_new, msg)

def log(message, display=False):
    """
    Devuelve por consola y escribe el log en el log file.
    """
    if display:
        print(message)
    with open(conf.LOGS, 'a') as f:
        f.write("\n"+message)
        f.close()

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    Clase servidor TCP.

    Note:   Esta clase hereda de la clase 'socketserver.BaseRequestHandler'
            Implementamos el metodo handle para intercambiar datos con el
            cliente.

    """
    def handle(self):

        local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

        #Cargamos el ultimo mensaje recibido al servidor
        self.data = self.request.recv(1024).strip().decode()
        #Comprobamos integridad del mensaje recibido
        cond = proof(self.data)
        print("{} sent:".format(self.client_address[0]))
        
        if cond[0]:

            message = local_time +" ["+self.client_address[0]+"]"+ " [notice] " + cond[3]
            log(message,True)
            print("Integridad correcta")
            print(self.data)
        else:

            message = local_time + "[ip:  "+self.client_address[0]+"]"+ " [error] " + cond[3]
            log(message,True)
            print("Fallo integridad: %s != %s " %(cond[1], cond[2]))
        # Devolvemos el ACK al cliente, confirmando el la llegada del mensaje
        self.request.sendall("ACK from TCP Server".encode())
    


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
     
    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    try:
        print("Servidor activo (HOST: %s ,PORT: %d)" %(HOST, PORT)) 
        tcp_server.serve_forever()

    except Exception as e:
        print("Error de apertura servidor: ",e)

    
