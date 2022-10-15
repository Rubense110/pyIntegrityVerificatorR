import os
import matplotlib.pyplot as plt
from fpdf import FPDF
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import conf

class Reports():
    """
    The purpose of this class is to create KPI graphics.
    """
    def __init__(self):
        self.report_data()
        self.craft_graphic()
        self.craft_pdf()
        try:
            self.craft_email()
        except:
            print("error enviando email")

    def report_data(self):
        with open(conf.LOGS, "r") as f:
            self.date = f.readlines()[-1].split(" ")[0].replace("/","-").strip("[")
            f = open(conf.ATTS_FROM_C_TO_S).readlines() 
            self.mitm_att, self.rep_att = (int(f[i].split(":")[1].strip()) for i in range(2))
            self.accesses = len(open(conf.LOGS, "r").readlines())-1
            self.accesses_na = self.accesses - ((self.mitm_att) +self.rep_att)

    def craft_graphic(self):
        values = [self.accesses_na, self.mitm_att, self.rep_att]
        legend = ["Transmissions w/o attacks", "Man in the Middle attacks", "Replay attacks"]
        f1 = {"family": "Arial","color": "black", "size": 20, "fontweight": "roman"}
        colors = ["lightskyblue", "lightcoral", "gold"]
        explode = [0, 0.2, 0.2]
        percentages = list()
        for i in values: percentages.append(100.*float(i)/sum(values))
        labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(legend, percentages)]
        plt.figure(figsize=(7,3))
        plt.pie(values,startangle=90,shadow=True,explode=explode,colors=colors)
        plt.title("Transmissions & Attacks\n",fontdict=f1)
        plt.legend(labels,loc="upper left",fontsize="x-small")
        plt.axis("equal")
        plt.savefig(os.path.join(conf.GRAPH_FOLDER,"graphic"+self.date+".png"),bbox_inches='tight',dpi=300)

    def craft_pdf(self):
        percentage = self.accesses_na / self.accesses
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 40)
        pdf.cell(200, 10, txt = "",ln = 1, align = 'C')
        pdf.cell(200, 10, txt = "INSEGUS",ln = 1, align = 'C')
        pdf.set_font('Times', 'B', 1)
        pdf.cell(200, 10, txt = "",ln = 1, align = 'C')
        pdf.set_font('Times', 'B', 40)
        pdf.cell(200, 10, txt = "INTEGRITY CHECK",ln = 1, align = 'C')
        pdf.set_font('Times', 'B', 16)
        pdf.cell(200, 10, txt = self.date+" report""\n\n" ,ln = 1, align = 'C')
        pdf.image(os.path.join(conf.GRAPH_FOLDER, "graphic"+self.date+".png"),20,60, h=100,w=180)
        pdf.cell(200, 100, txt = "",ln = 1, align = 'L')
        pdf.set_left_margin(32)
        pdf.set_font("Times",style="")
        pdf.cell(200, 20, txt = "",ln = 1, align = 'C')
        pdf.cell(200, 10, txt = "· Nº of Man in the Middle attacks detected: "+str(self.mitm_att),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Nº of Replay attacks detected: "+str(self.rep_att),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Nº of total transmissions: "+str(self.accesses),ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· KPI = (transmissions w/o attacks) / total transmissions",ln = 1, align = 'L')
        pdf.cell(200, 10, txt = "· Percentage of transmissions w/o attacks (KPI): "+str("{:%}".format(percentage)),ln = 1, align = 'L')
        pdf.output(os.path.join(conf.PDF_FOLDER,"report-"+self.date+".pdf"), "F")

    def craft_email(self):
        message = MIMEMultipart()
        message["From"]= "mail@attacks.pai"
        message["To"]= "sysadmin@attacks.com"
        message["Subject"]= "Transmissions'_Integrity_Report"+self.date
        text_message = MIMEText("The pdf file with the transmissions report is attached. \n Best regards.")
        message.attach(text_message)

        pdfname= "report-"+self.date+".pdf"
        pdf = open(os.path.join(conf.PDF_FOLDER,"report-"+self.date+".pdf"), "rb")
        payload = MIMEBase("application","octate-stream",Name = pdfname )
        payload.set_payload(pdf.read())
        encoders.encode_base64(payload)
        payload.add_header('Content-Decomposition', 'attachment', filename=pdfname)
        message.attach(payload)

        connection = smtplib.SMTP(host="localhost",port= 2500)
        connection.sendmail(from_addr="mail@attacks.pai", to_addrs="sysadmin@attacks.com",msg=message.as_string())

        connection.quit()
        
Reports()