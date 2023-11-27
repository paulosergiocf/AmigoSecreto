from dataclasses import dataclass
import smtplib

@dataclass
class Email:
    destinatario: str
    assunto: str
    corpo: str
    
