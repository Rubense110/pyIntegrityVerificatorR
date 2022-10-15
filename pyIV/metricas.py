import subprocess
import os
import time



subprocess.Popen("server.exe" ,shell=True)

tiempo1 = time.time()
i = 0
while(i<1):
    exec(open("client2.py").read())
    i += 1
tiempo2 = time.time()

tiempo = tiempo2-tiempo1
print(tiempo)
os.system("taskkill /f /im  server.exe")