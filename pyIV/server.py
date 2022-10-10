import socketserver

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    Clase servidor TCP.

    Note:   Esta clase hereda de la clase 'socketserver.BaseRequestHandler'
            Implementamos el metodo handle para intercambiar datos con el
            cliente.

    """

    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(5000).strip()

        print("{} sent:".format(self.client_address[0]))
        print(self.data)
        # just send back ACK for data arrival confirmation
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
        print("Error de apertura: ",e)
    
