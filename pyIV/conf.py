import os

PATH = os.path.abspath(".")

#Path para el log del servidor
LOGS = os.path.join(PATH,"logs","log.txt")

#Path para base de nonces servidor
NONCE_SERV = os.path.join(PATH,"nonces","nonces_serv")
#Path para base de nonces cliente
NONCE_CLNT = os.path.join(PATH,"nonces","nonces_clnt")
ERROR_SERV = os.path.join(PATH,"logs","error_log.txt")