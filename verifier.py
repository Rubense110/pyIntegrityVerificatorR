import hmac
import hashlib
import pickle
import os

import conf

ncliente = conf.NONCE_CLNT
nserver = conf.NONCE_SERV
clave = "123456"

class Verifier():
    def __init__(self, data, sv= False):    # IMPORTANTE: No alterar el orden de los atributos y metodos en el constructor
        self.nonces = []
        self.basenonces = ncliente if sv == False else nserver
        self.loadNonces()
        self.data = data
        self.key = clave
        self.proof()

    def proof(self):
        msg, nonce, hash_old = self.data.split("|")
        hash_new =  hmac.new(self.key.encode(),(msg+nonce).encode(), hashlib.sha256).hexdigest()

        if nonce not in self.nonces:
            self.nonces.append(nonce)
            if hash_old==hash_new: res = 0
            else: res = 2
        else: res = 1

        if self.basenonces == nserver :
            if res==0:      self.msgSv = "ACK from TCP Server";         self.logData = " [notice] "
            elif res==1:    self.msgSv = "Rechazado, Replay detectado"; self.logData = " [rp_error] "
            else:           self.msgSv = "Rechazado, MitM detectado";   self.logData = " [int_error] "

        else:
            if res==0:      print("Integridad correcta\n")       
            elif res==1:    print("Incidencia de tipo 'Reply' detectada\n")
            else:           print("Incidencia de tipo 'Integridad' detectada\n")

        self.WritteNonces()

    def WritteNonces(self):
        with open(self.basenonces,"wb") as f:
            pickle.dump(self.nonces,f)
            f.close()           

    def loadNonces(self):
        if os.path.exists(self.basenonces):
            with open(self.basenonces,"rb") as f:
                self.nonces += pickle.load(f)
        