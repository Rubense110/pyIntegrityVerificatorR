from copyreg import pickle
import socketserver
import hmac
import hashlib
import time
import secrets
import random
import pickle
import os

import conf
from verifier import Verifier

class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    TCP Server class.

    Note:   This class inherits from the class 'socketserver.BaseRequestHandler'.
            We implement the handle method to exchange data with the client.
    """
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    def handle(self): 
        self.error_file()
        local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

        self.nonce = secrets.token_urlsafe()
        self.data = self.request.recv(1024).strip().decode()   # Last message received is loaded  
        
        print("\n{} sent:".format(self.client_address[0]))
        self.verif = Verifier(self.data, sv= True)          # Integrity check of the received message
        self.message = local_time +" ["+self.client_address[0]+"]"+ self.verif.logData + self.data.split("|")[0]
        self.msg= self.verif.msgSv[0]

        if self.verif.msgSv[1] == 0: pass
        elif self.verif.msgSv[1] == 1: self.err_rep +=1
        else: self.err_mitm +=1

        self.server_response()
        self.write_error()

    def error_file(self): # Error log file
        if os.path.exists(conf.ERROR_SERV):
            f = open(conf.ERROR_SERV, "r")
            errors_list = [l.split(":")[1].strip() for l in f]
            self.err_mitm = int(errors_list[0])
            self.err_rep = int(errors_list[1])
            f.close()
        else:
            with open(conf.ERROR_SERV,"w") as f:
                f.write("mitm_error : 0\nreplay_error : 0")
                f.close()
    
    def write_error(self): # Accumulative errors
        errors =[self.err_mitm, self.err_rep]
        replacement = ""
        f_read = open(conf.ERROR_SERV, "r")
        i =0
        for line in f_read.readlines():
            s_line = line.split(":")
            replacement += s_line[0]+": "+ str(errors[i])+"\n"
            i+=1
        f_read.close()
        fout = open(conf.ERROR_SERV, "w+")
        fout.write(replacement)
        fout.close()

    def server_response(self):
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
        
        hash_new =  hmac.new(self.verif.key.encode(),(self.msg+self.nonce).encode(), hashlib.sha256).hexdigest()
        response =  "|".join([self.msg2,self.nonce,hash_new])
        self.request.sendall(response.encode())
        self.log(self.message,True)  
        print("Server Response: ",self.msg2) 

    def log(self,mensaje,display=False):
        """
        Returns by console and writes the log in the log file.
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