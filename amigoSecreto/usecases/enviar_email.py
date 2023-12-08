import os
import smtplib
from email.mime.text import MIMEText
from amigoSecreto.entities.email import Email
from dotenv import load_dotenv
load_dotenv()

class ServidorEmail:
    def __init__(self):
        self.__remetente = str(os.getenv('OUTLOOKMAIL'))
        self.__pass = str(os.getenv('OUTLOOKPASS'))
        self.__servidor = str(os.getenv('OUTLOOKSERVERSMTP'))
        self.__porta = str(os.getenv('OUTLOOKSERVERSMTPPORTA'))
        self.__conexao = smtplib.SMTP(self.__servidor, self.__porta)
    
    
    def login(self):
        self.__conexao.starttls()
        self.__conexao.login(self.__remetente, self.__pass)
        
    
    def fecharConexao(self):
        self.__conexao.quit()
        
    def enviarEmail(self, email: Email):
        self.login()
        mensagem = self.formatarEmail(email)
        self.__conexao.sendmail(self.__remetente, 
                       email.destinatario, 
                       mensagem.as_string())
        self.fecharConexao()
        
    def formatarEmail(self, email: Email):
        mensagem = MIMEText(email.corpo)
        mensagem["From"] = os.getenv('OUTLOOKMAIL')
        mensagem["To"] = email.destinatario
        mensagem["Subject"] = email.assunto
        
        return mensagem
    
