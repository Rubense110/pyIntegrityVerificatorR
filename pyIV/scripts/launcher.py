import time
import os
import subprocess

import conf
from client import Handler_TCPClient

if __name__ == "__main__":

        print("Welcome to INSEGUS' configuration environment\n \
            \nWhat would you like to do?")
        print("[1] Turn on the system")
        print("[2] Set audit period")
        print("[3] Server audit")
        print("[4] Exit configuration\n")

        case = int(input("Choose option: "))
        
        while case >4 or case==0:
            case = int(input("You can choose between [1 | 2 | 3], choose option: "))

        if case == 1:
            print("Turning on the system...")
            print("Turning on the server...\n")
            
            key= "d05eb090b65a8bc751b5790133a70eb2"
            host_ip, server_port = "127.0.0.1", 9999
            subprocess.Popen("server.exe" ,shell=True)
            time.sleep(2)
            
            print("Make bank transfer \n")
            src_acc = input("Enter source account (6 digits): ")
            dst_acc = input("Enter destination account (6 digits): ")
            qtt = input("Enter the quantity to send: ")
            msg = src_acc+" "+dst_acc+" "+qtt
            print("\n Transfer: ", msg)
            
            print("\n Actions to be performed: ")
            print("[1] Send transfer")
            print("[2] MitM Attack simulation")
            print("[3] Replay Attack simulation")
            case1 = int(input("Choose option: "))

            while case1 >3 or case1==0:
                case1 = int(input("You can choose between [1 | 2 | 3], choose option: "))

            if case1 == 1:
                print("####### Transferring... #######\n")
                a1 = Handler_TCPClient(host_ip,server_port,msg,key)
                try:
                    a1.send()
                except:
                    os.system("taskkill /f /im  server.exe")
                
            elif case1 == 2:
                print("####### MitM Attack simulation #######\n")

                print("Modifying original message...\n")
                print("Original source account: ", src_acc)
                src_acc1 = input("Enter source account (6 digits): ")
                print("\nOriginal destination account: ",dst_acc)
                dst_acc1 = input("Enter destination account (6 digits): ")
                print("\nOriginal amount : ", qtt)
                qtt1 = input("Enter quantity to send: ")
                msg1 = src_acc1+" "+dst_acc1+" "+qtt1
                print("\n Transfer modified ^_^: ", msg1)
                a2 = Handler_TCPClient(host_ip,server_port,msg,key)
                try: 
                    a2.mitm(msg1)
                except Exception as e:
                    os.system("taskkill /f /im  server.exe")
            else:
                print("####### Replay Attack simulation #######\n")
                
                reps = int(input("Enter the number of message replications: "))
                a3 = Handler_TCPClient(host_ip,server_port,msg,key)
                try:
                    a3.replay(reps)
                except Exception as e:
                    os.system("taskkill /f /im  server.exe")

            print("Shutting down the server...")
            time.sleep(2)
            os.system("taskkill /f /im  server.exe")
            print("Leaving...")
            time.sleep(1.5)
            exit(0)
                
        elif case == 2:
            print("Setting audit period...")
            print("Daily reviews are perfomed")
            hday = input("Set revision time: ")
            os.system(conf.TASKSC+hday)
        elif case == 3:
            print("Performing server audit...")
            print("It may take a few seconds...")
            subprocess.run("reports.exe")
        else:
            print("Leaving...")
            time.sleep(1)
            exit(0)
