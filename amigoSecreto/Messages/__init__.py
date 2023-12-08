from enum import Enum

class Mensagens(Enum):
    VERSION = 'v1.00'
    EMAIL_PENDENTE = """
    Olá ####, seu pedido de aprovação para participar do 
    amigo secreto na sala $$$$ está pendente!
    
    você pode acompanhar seu status na pagina da sala.
    """
    LOGIN_CRIAR_SALAS = "É necessário fazer o login para criar salas."
    CRIACAO_RESPONSAVEL = "Parabens ####, agora pode fazer login em sua conta e criar suas próprias salas."
    
    
    
    
    