from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaSorteio, SalaParticipante
from amigoSecreto.Messages import Mensagens
from amigoSecreto.entities.email import Email
from amigoSecreto.usecases.enviar_email import ServidorEmail

import random

## --------------- Participante util-------------
def verificarParticipante(nome, email):
    try:
        participante = Participante.objects.get(email=email)
    except Participante.DoesNotExist:
        participante = Participante.objects.create(nome=nome, email=email)
    finally:
        return participante

def adicionarParticipanteResponsavelSala(responsavel, sala):
    try:
        participante = verificarParticipante(responsavel.username, responsavel.email)
        novo_participante_sala = SalaParticipante(codigoSala=sala, participante=participante, valido=True)
        novo_participante_sala.save()
        return True, 'sucesso.'
    
    except Exception as erro:
        return False, erro
    
def adicionarParticipanteSala(nome, email, sala):
    try:
        participante = verificarParticipante(nome, email,)
        novo_participante_sala = SalaParticipante(codigoSala=sala, participante=participante, valido=False)
        novo_participante_sala.save()
        return True, 'sucesso.'
    
    except Exception as erro:
        return False, erro
    
## --------------- Envio de emails-----------------#
def emailParticipanteCadastrado(participante, codigo):
    try:
        destinatario = participante.email
        assunto = f"Email - inscrição amigo secreto Sala {codigo}"
        corpo = Mensagens.EMAIL_PENDENTE.value
        corpo = corpo.replace("####",participante.nome).replace("$$$$", codigo)
        email = Email(destinatario,assunto, corpo)
        serverEmail = ServidorEmail()
        serverEmail.enviarEmail(email=email)
        return True, f'email enviado com sucesso para {destinatario}'
        
    
    except Exception as erro:
        return False, erro
    

def emailParticipanteResponsavelCadastrado(responsavel):
    try:
        destinatario = responsavel.email
        assunto = f"Email - Criação de conta"
        corpo = Mensagens.CRIACAO_RESPONSAVEL.value
        corpo = corpo.replace("####",responsavel.username)
        email = Email(destinatario ,assunto, corpo)
        serverEmail = ServidorEmail()
        serverEmail.enviarEmail(email=email)
        return True, f'email enviado com sucesso para {responsavel.username}'
        
    
    except Exception as erro:
        return False, erro
    

def enviarEmailSorteados(sorteados):
    VSSENHORIA= "$$$$"
    AMIGOSECRETO = "####"
    MENSAGENS_AMIGO_SECRETO = [
        """Olá, $$$$. 
        A baleia-azul é responsável pelo som mais alto do mundo. 
        Sua voz pode ser ouvida até 800 km de distância. Ela só não ganha do seu amigo secreto #### gritando quando ganha algo que não gosta.""",
        
        """Olá, $$$$.
        Sem luzes para o Natal? Fiquei suave! A Maganize Luiza tem as melhores opções para você! Compre uma geladeira para #### no Natal e a encha. Você não pode perder a nossa oferta e perder a chance de ver o rosto se iluminar tanto, mais tanto, que nem vai precisar de pisca-pisca para a ceia.""",
       
        """Olá, $$$$.
        De lá para cá, de cá para lá, por onde vamos, carregamos conosco milhões de bactérias, e seu amigo secreto, que atende pelo nome de ####, também. 
        ja parou para pensar que talvez sejamos apenas um meio de transporte para elas?""",
        
        """Olá, $$$$.
        O bico do ornitorrinco consegue detectar campos elétricos de outros seres vivos, fazendo com que ele tenha um sexto sentido para conseguir caçar e se mover. 
        Ele consegue confiar completamente em seu bico, assim como seu amigo secreto #### confia que você não vai dar um par de meias para ele.""",
        
        """Olá, $$$$.
        Seu amigo secreto é um animal mamífero, bípede, que se distingue dos demais mamíferos pelo telencéfalo altamente desenvolvido e o polegar opositor. Atende pelo nome de ####""",
        
        """Olá, $$$$.
        Se é pavê ou pacomê?
        Pacomê eu não sei, mas pavê presente para ####, você vai ter que correr.""",
        """
        Olá, $$$$

        Te apresento seu amigo secreto ####.
        De onde ele veio?
        De trás do bananal
        E o que ele merece?
        Um presente bem legal.
        """,
        
        """Olá, $$$$.
        Se ovo veio primeiro que a galinha, ou se a galinha veio primeiro que o ovo, eu não sei. 
        Mas sei que #### é seu amigo secreto, e isso me chocou. """,
        
        """Olá, $$$$.
        O aquecimento global ta aí, e todo mundo vai ser assado, então por que não contribuir para esse processo ser mais rápido? 
        É muito fácil para ajudar, de um presente para #### e veja seu coração aquecer como o planeta, ele vai aquecer tanto que vai morrer de felicidade  :D"""
    ]
    controle = list()
    try:
        for destinatario, amigoSecreto in sorteados.items():
        
            assunto = f"Seu amigo secreto é...."
            corpo = random.choice(MENSAGENS_AMIGO_SECRETO)
            corpo = corpo.replace(AMIGOSECRETO,amigoSecreto.nome).replace(VSSENHORIA, destinatario.nome)
            email = Email(destinatario.email, assunto, corpo)
            serverEmail = ServidorEmail()
            serverEmail.enviarEmail(email=email)
            controle.append(f'email enviado com sucesso para {destinatario.nome}')
    
    except Exception as erro:
        return erro
    else:
        return True if len(sorteados) == len(controle) else Exception("não foi possivel enviar todos os emails")

    