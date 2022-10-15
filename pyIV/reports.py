import conf
import os
import matplotlib.pyplot as plt

class reports():

    def __init__(self):
        
        self.report_data()
        self.craftea_grafico()

    def report_data(self):
        with open(conf.LOGS, "r") as f:
            self.fecha = f.readlines()[-1].split(" ")[0].strip("[")
            f = open(conf.ERROR_SERV).readlines() 
            self.err_int, self.err_rep = (int(f[i].split(":")[1].strip()) for i in range(2))
            self.accesos = len(open(conf.LOGS, "r").readlines())-1
            self.accesos_sin = self.accesos - ((self.err_int) +self.err_rep)

    def craftea_grafico(self):
        valores = [self.accesos_sin, self.err_int, self.err_rep]
        print(valores)
        legend =  ["Accesos sin incidencia", "Incidencias de Integridad", "Incidencias de Replay"]
        f1=       {"family": "Arial","color": "black", "size": 20, "fontweight": "roman"}
        colors =  ["lightskyblue", "lightcoral", "gold"]
        explode = [0, 0.2, 0.2]
        
        porcent= list()
        for i in valores: porcent.append(100.*float(i)/sum(valores))
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(legend, porcent )]
        plt.figure(figsize=(7,3))
        plt.pie(valores,startangle=90,shadow=True,explode=explode, colors=colors)
        plt.title("Accesos al Servidor\n",fontdict=f1)
        plt.legend(labels,loc="upper left",fontsize="x-small")
        plt.axis("equal")
        plt.savefig(os.path.join(conf.GRAPH_FOLDER, "grafico"+self.fecha.replace("/","-")+".png"),bbox_inches='tight',dpi=300)



reports()