import time
import os
import subprocess

import conf
from client import Handler_TCPClient

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
#            exec(open(os.path.join(conf.PATH,"client.py")).read())
            
            print("Realizar transferencia bancaria \n")
            cuenta_org = input("Introduce cuenta origen (6 digitos) : ")
            cuenta_dest = input("Introduce cuenta destino (6 digitos) : ")
            cantidad = input("Introduce la cantidad a mandar: ")
            msg = cuenta_org+" "+cuenta_dest+" "+cantidad
            print("\n Transferencia: ", msg)
            
            print("\n Acciones a realizar: ")
            print("[1] Envio de transferencia")
            print("[2] Simulacion ataque MitM")
            print("[3] Simulacion ataque de Replay")
            case1 = int(input("Escoja opcion: "))

            while case1 >3 or case1==0:
                case1 = int(input("Debe escoger entre [1 | 2 | 3], escoja opcion: "))

            if case1 == 1:
                print("####### Realizando la transferencia... #######\n")
                a1 = Handler_TCPClient(host_ip,server_port,msg,key)
                try:
                    a1.send()
                except:
                    os.system("taskkill /f /im  server.exe")
                
            elif case1 == 2:
                print("####### Simulacion ataque MitM #######\n")

                print("Modificar el mensage original...\n")
                print("Cuenta origen original: ",cuenta_org)
                cuenta_org1 = input("Introduce cuenta origen (6 digitos) : ")
                print("\nCuenta destino original: ",cuenta_dest)
                cuenta_dest1 = input("Introduce cuenta destino (6 digitos) : ")
                print("\nCantidad original: ", cantidad)
                cantidad1 = input("Introduce la cantidad a mandar: ")
                msg1 = cuenta_org1+" "+cuenta_dest1+" "+cantidad1
                print("\n Transferencia modificada ^_^: ", msg1)
                a2 = Handler_TCPClient(host_ip,server_port,msg,key)
                try: 
                    a2.mitm(msg1)
                except Exception as e:
                    os.system("taskkill /f /im  server.exe")
            else:
                print("####### Simulación ataque de Replay #######\n")
                
                reps = int(input("Introducir el numero de repeticiones del mensaje: "))
                a3 = Handler_TCPClient(host_ip,server_port,msg,key)
                try:
                    a3.replay(reps)
                except Exception as e:
                    os.system("taskkill /f /im  server.exe")


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
