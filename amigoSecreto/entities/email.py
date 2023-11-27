from dataclasses import dataclass

@dataclass
class Email:
    destinatario: str
    assunto: str
    corpo: str
    
