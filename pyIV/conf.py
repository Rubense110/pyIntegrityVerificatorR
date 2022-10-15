import os

PATH = os.path.abspath(".")    # Absolute path
LOGS = os.path.join(PATH,"logs","log.txt")
NONCE_SERV = os.path.join(PATH,"nonces","nonces_serv")
NONCE_CLNT = os.path.join(PATH,"nonces","nonces_clnt")
ATTS_FROM_C_TO_S = os.path.join(PATH,"logs","att_log.txt")
GRAPH_FOLDER = os.path.join(PATH,"reports", "graphs")
PDF_FOLDER = os.path.join(PATH,"reports")
