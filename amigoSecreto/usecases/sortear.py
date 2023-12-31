import random
from amigoSecreto.models import Participante
from amigoSecreto.usecases.regras import enviarEmailSorteados

class AmigoSecreto:
    def __init__(self, max_tentativas=10) -> None:
        self.__max_tentativas = max_tentativas
        
    def sortear(self, participantes):
        if len(participantes) <=1:
            raise ValueError('é nescessário dois participantes ou mais para efetuar o sorteio.')
        
        flag = True
        while flag:
            try:
                sorteados = self.__executar(participantes)
                flag = False
            except ValueError as erro:
                pass
            
        return sorteados
    
    def __executar(self, participantes: list):
        """_summary_

        Args:
            participantes (list): lista de participantes

        Raises:
            ValueError: lançãdo caso ocorra um problema que prenda um sorteio em loop por 10 vezes.

        Returns:
            list: resultado sorteio
        """
        para_sortear = participantes.copy()
        sorteio = dict()
        tentativas = 0
        
        for participante in participantes:
            if len(para_sortear) == 2 and participante in para_sortear:
                sorteado = para_sortear[1] if participante == para_sortear[0] else para_sortear[0]
            else:
                sorteado = random.choice(para_sortear)
                while participante == sorteado:
                    sorteado = random.choice(para_sortear)
                    tentativas += 1
                    if tentativas == self.__max_tentativas:
                        raise ValueError('erro não tratado')

            sorteio[participante] = sorteado
            para_sortear.remove(sorteado)

        return sorteio

    

def executarSorteio(participantes):
    lista = extrairParticipante(participantes)
    
    try:
        amigoSecreto = AmigoSecreto()
        sorteados = amigoSecreto.sortear(lista)
        enviarEmailSorteados(sorteados)
    except Exception as erro:
        return erro
    else:
        True
        
def extrairParticipante(participantes):
    participantesExtraidos = list()
    for participante in participantes:
        participantesExtraidos.append(participante)
    
    return participantesExtraidos