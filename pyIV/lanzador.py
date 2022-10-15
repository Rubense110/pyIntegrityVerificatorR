import time
import os
import subprocess

import conf

if __name__ == "__main__":

        print("Bienvenido al entorno de configuración INSEGUS\n \
            \n¿Qué desea realizar?")
        print("[1] Poner en marcha el sistema")
        print("[2] Establecer periodo de auditoria")
        print("[3] Auditoria del servidor")
        print("[4] Salir de la configuración\n")

        case = int(input("Escoja opción: "))
        
        while case >4 or case==0:
            case = int(input("Debe escoger entre [1 | 2 | 3], escoja opción: "))

        if case == 1:
            print("Poniendo en marcha el sistema...")
            print("Encendiendo el servidor...\n")
            
            key= "123456"
            host_ip, server_port = "127.0.0.1", 9999
            subprocess.Popen("server.exe" ,shell=True)
            time.sleep(2)

            #Ejecutamos el cliente
            exec(open(os.path.join(conf.PATH,"client.py")).read())

            print("Apagando el servidor...")
            time.sleep(2)
            os.system("taskkill /f /im  server.exe")
            print("Saliendo...")
            time.sleep(1.5)
            exit(0)
        elif case == 2:
            print("Estableciendo periodo de auditoria..")
            print("Se realizan revisiones diarias")
            horaDia = input("Establecer hora de revision: ")
            os.system(conf.TASKSC+horaDia)
        elif case == 3:
            print("Realizando auditoria del servidor...")
            print("Puede tardar unos segundos...")
            subprocess.run("reports.exe")
        else:

            print("Saliendo..")
            time.sleep(1)
            exit(0)
