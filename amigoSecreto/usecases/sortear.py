import random

class AmigoSecreto:
    def __init__(self, max_tentativas=10) -> None:
        self.__max_tentativas = max_tentativas
        
    def sortear(self, participantes):
        flag = True
        while flag:
            try:
                sorteados = self.__executar(participantes)
                flag = False
            except ValueError as erro:
                pass
            
        return sorteados
    
    def __executar(self, participantes: list):
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
                        raise ValueError('deu ruim')

            sorteio[participante] = sorteado
            para_sortear.remove(sorteado)

        return sorteio

    