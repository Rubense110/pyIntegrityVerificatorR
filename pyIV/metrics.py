import subprocess
import os
import time
import matplotlib.pyplot as plt
import numpy as np

from client import Handler_TCPClient as handler


key= "123456"
host_ip, server_port = "127.0.0.1", 9999
msg = "16272727 17172772 20000"
msg2= "16272728 17172772 2000000"

def time_calc(messages,code=0):
    """
    Returns a dictionary {msg_index : time value} with the access time 
    for each message inidicated on the input
    code = 1 for MitM attacks and code = 2 for Replay attacks
    """
    subprocess.Popen("server.exe" ,shell=True)
    res = {}
    if code == 1:
            i = 0
            while(i<messages):
                time1 = time.time()
                handler(host_ip, server_port, msg, key).mitm(msg2)
                i += 1
                if(i>1): time2 = time.time(); res[i] = time2-time1

    elif code == 2:
            i = 0
            while(i<messages):
                time1 = time.time()
                handler(host_ip, server_port, msg, key).replay(4)
                i += 1
                if(i>1): time2 = time.time(); res[i] = time2-time1

    else :
            i = 0
            while(i<messages):
                time1 = time.time()
                handler(host_ip, server_port, msg, key).send()
                i += 1
                if(i>1): time2 = time.time(); res[i] = time2-time1
    os.system("taskkill /f /im  server.exe")
    return res


def avg_metric_graph():
    """
    Returns a bar graph showing the access time of 100 regular messages and 100 MitM modified messages alongside their average values
    """
    regular_time_access = time_calc(100)
    MitM_time_access = time_calc(100,code=1)


    x = list(regular_time_access.keys())
    y = list(regular_time_access.values())

    y1= list(MitM_time_access.values())
    co = np.arange(len(x))
    
    plt.bar(co-0.2,y,width=0.4,color = "lightskyblue",label="regular msgs")
    plt.bar(co+0.2,y1,width=0.4, color = "lightcoral", label= "MitM msgs")
    plt.xlabel("Server messages ")
    plt.ylabel("Response time (seconds)")
    plt.title("Server Performance Test (100 messages)")

    plt.axhline(y=np.nanmean(y), color='black', linestyle='--', linewidth=3, label= "avg regular msg ="+(str(round(np.nanmean(y)*1000))+" miliseconds"))
    plt.axhline(y=np.nanmean(y1), color='gray', linestyle='--', linewidth=3, label= "avg MitM="+(str(round(np.nanmean(y1)*1000))+" miliseconds"))
    plt.legend()
    plt.show()


avg_metric_graph()