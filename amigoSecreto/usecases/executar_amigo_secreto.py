from amigoSecreto.usecases.enviar_email import ServidorEmail
from amigoSecreto.usecases.sortear import AmigoSecreto


class ExeAmigoSecreto:
    def __init__(self, participantes: list):
        self.__participantes = participantes
        
        
    def executar(self):
        sortear = AmigoSecreto()
        
        flag = False
        while flag:
            try:
                sorteados = sortear.sortear(self.__participantes)
                flag = True
            except ValueError as erro:
                pass
        
        servidor = ServidorEmail()
        
        