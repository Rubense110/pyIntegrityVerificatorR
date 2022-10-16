import subprocess
import os
import time
from client import Handler_TCPClient as handler


subprocess.Popen("server.exe" ,shell=True)
key= "QfTjWnZr4u7x!A%D"
host_ip, server_port = "127.0.0.1", 9999
time1 = time.time()
msg = "16272727 17172772 20000"
msg2= "16272728 17172772 2000000"

i = 0
while(i<10000):
    handler(host_ip, server_port, msg, key).send()
    handler(host_ip, server_port, msg, key).mitm(msg2)
    handler(host_ip, server_port, msg, key).replay(4)
    i += 1
time2 = time.time()

ftime = time2-time1
print(ftime)
os.system("taskkill /f /im  server.exe")