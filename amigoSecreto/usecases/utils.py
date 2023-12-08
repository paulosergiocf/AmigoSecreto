from datetime import date, datetime

def gerarDiagramacao(lista):
    """
    Args:
        lista: de dados.
    Returns:
        lista: lista com matriz para prencher tela em tres colunas.
    """
    lista_diagramar =list()
    for resultado in lista:
        lista_diagramar.append(resultado)
    
    envelope= list()
    diagramacao = dict()
    contador = 1
    linha = 1
    for objeto in lista_diagramar:
        if contador == 1:
            diagramacao[f"linha{linha}"] = [objeto]
            contador +=1
        elif contador == 2:
            diagramacao[f"linha{linha}"].append(objeto)
            contador +=1
        elif contador == 3:
            diagramacao[f"linha{linha}"].append(objeto)
            linha += 1
            contador = 1 

        envelope.append(diagramacao)

    return diagramacao

def formatar(data_obj):
    data_string = data_obj.strftime('%Y-%m-%d')
    datalista = data_string.split('-')
    data = date(int(datalista[0]), int(datalista[1]), int(datalista[2]))
    return data