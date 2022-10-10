import socket
import hmac
import hashlib

host_ip, server_port = "127.0.0.1", 9999
data = "16272727 17172772 20000 "

key= "123456"
msg_hmac = hmac.new(key.encode(),data.encode(), hashlib.sha256).hexdigest()

# Initialize a TCP client socket using SOCK_STREAM
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Establish connection to TCP server and exchange data
    tcp_client.connect((host_ip, server_port))
    tcp_client.sendall(data.encode())

    # Read data from the TCP server and close the connection
    received = tcp_client.recv(1024)
finally:
    tcp_client.close()

print ("Bytes Sent:     {}".format(data+msg_hmac))
print ("Bytes Received: {}".format(received.decode()))