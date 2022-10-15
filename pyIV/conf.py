import os

PATH = os.path.abspath(".") # Absolute path
LOGS = os.path.join(PATH,"logs","log.txt")
NONCE_SERV = os.path.join(PATH,"nonces","nonces_serv")
NONCE_CLNT = os.path.join(PATH,"nonces","nonces_clnt")
ERROR_SERV = os.path.join(PATH,"logs","error_log.txt")
GRAPH_FOLDER = os.path.join(PATH,"reports", "graphs")
PDF_FOLDER = os.path.join(PATH,"reports")
