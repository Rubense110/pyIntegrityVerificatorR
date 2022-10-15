import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import conf

class reports():

    def __init__(self):
        
        self.report_data()
        self.craftea_grafico()
        self.craftea_pdf()
        self.craftea_email()

    def report_data(self):
        with open(conf.LOGS, "r") as f:
            self.fecha = f.readlines()[-1].split(" ")[0].replace("/","-").strip("[")
            f = open(conf.ERROR_SERV).readlines() 
            self.err_int, self.err_rep = (int(f[i].split(":")[1].strip()) for i in range(2))
            self.accesos = len(open(conf.LOGS, "r").readlines())-1
            self.accesos_sin = self.accesos - ((self.err_int) +self.err_rep)

    def craftea_grafico(self):
        valores = [self.accesos_sin, self.err_int, self.err_rep]
        print(self.fecha)
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
        plt.savefig(os.path.join(conf.GRAPH_FOLDER, "grafico"+self.fecha+".png"),bbox_inches='tight',dpi=300)

    def craftea_pdf(self):
        porcentaje_integro = self.accesos_sin / self.accesos

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 40)
        pdf.cell(200, 10, txt = "",ln = 1, align = 'C')
        pdf.cell(200, 10, txt = "INTEGRIDAD INSEGUS",ln = 1, align = 'C')
        pdf.set_font('Times', 'B', 16)
        pdf.cell(200, 10, txt = "Reporte "+self.fecha+"\n\n" ,ln = 1, align = 'C')
        pdf.image(os.path.join(conf.GRAPH_FOLDER, "grafico"+self.fecha+".png"),20,50, h=100,w=180)
        pdf.cell(200, 100, txt = "",ln = 1, align = 'L')
        pdf.set_left_margin(32)
        pdf.set_font("Times",style="")
        pdf.cell(200, 20, txt = "",ln = 1, align = 'C')
        pdf.cell(200, 10, txt = "· Nº de errores de Integridad detectados: "+str(self.err_int),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Nº de errores de replay detectados: "+str(self.err_rep),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Nº total de accesos: "+str(self.accesos),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· KPI = accesos sin incidencia / accesos totales",ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Porcentaje de incidencias (KPI): "+str("{:%}".format(porcentaje_integro)),ln = 1, align = 'L')
        pdf.output(os.path.join(conf.PDF_FOLDER,"reporte-"+self.fecha+".pdf"), "F")

    def craftea_email(self):
        
        mensaje = MIMEMultipart()
        mensaje["From"]= "correo@hids.pai"
        mensaje["To"]= "sysadmin@hids.com"
        mensaje["Subject"]= "Reporte de accesos HIDS "+self.fecha
        mensaje_texto = MIMEText("Se adjunta el archivo pdf con el reporte de accesos. \n Le enviamos un Cordial saludo.")
        mensaje.attach(mensaje_texto)

        pdfname= "reporte-"+self.fecha+".pdf"
        pdf = open(os.path.join(conf.PDF_FOLDER,"reporte-"+self.fecha+".pdf"), "rb")
        payload = MIMEBase("application","octate-stream",Name = pdfname )
        payload.set_payload(pdf.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
        mensaje.attach(payload)

        conexion = smtplib.SMTP(host="localhost",port= 2500)
        conexion.sendmail(from_addr="correo@hids.pai", to_addrs="sysadmin@hids.com",msg=mensaje.as_string())
        conexion.quit()
reports()