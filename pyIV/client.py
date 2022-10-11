import socket
import hmac
import hashlib
import random
import secrets

host_ip, server_port = "127.0.0.1", 9999

#Cuerpo mensaje al servidor
msg = "16272727 17172772 20000"
key= "123456"
nonce = secrets.token_urlsafe()
msg_hmac = hmac.new(key.encode(), (msg+nonce).encode(), hashlib.sha256).hexdigest()
data = msg +" | "+ nonce +" | "+ msg_hmac

x = random.random()

if x<=2/3:
    y = random.random()
    # Initialize a TCP client socket using SOCK_STREAM
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        if y<0.5:
            print("MitM")
            #Establecemos conexion con el servidor TCP para simular ataque de integridad (MitM)
            new_msg = "16272728 17172772 2000000"
            data = new_msg +" | "+ data.split("|")[1].strip() +" | "+ data.split("|")[2].strip()
            tcp_client.connect((host_ip, server_port))
            tcp_client.sendall(data.encode())
        else:
            print("normal")
            # Establish connection to TCP server and exchange data
            tcp_client.connect((host_ip, server_port))
            tcp_client.sendall(data.encode())

        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()

    print ("Bytes Sent:     {}".format(data))
    print ("Bytes Received: {}".format(received.decode()))


else:
    i = 0
    while(i<2):
        # Initialize a TCP client socket using SOCK_STREAM
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print("replay")
            # Establish connection to TCP server and exchange data
            tcp_client.connect((host_ip, server_port))
            tcp_client.sendall(data.encode())
            # Read data from the TCP server and close the connection
            received = tcp_client.recv(1024)
        finally:
            tcp_client.close()

        print ("Bytes Sent:     {}".format(data))
        print ("Bytes Received: {}".format(received.decode()))
        i=i+1


