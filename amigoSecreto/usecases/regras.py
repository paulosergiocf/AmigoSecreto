from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaSorteio, SalaParticipante
from amigoSecreto.Messages import Mensagens
from amigoSecreto.entities.email import Email
from amigoSecreto.usecases.enviar_email import ServidorEmail

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
        novo_participante_sala = SalaParticipante(codigoSala=sala, email=participante, valido=True)
        novo_participante_sala.save()
        return True, 'sucesso.'
    
    except Exception as erro:
        return False, erro
    
def adicionarParticipanteSala(nome, email, sala):
    try:
        participante = verificarParticipante(nome, email,)
        novo_participante_sala = SalaParticipante(codigoSala=sala, email=participante, valido=False)
        novo_participante_sala.save()
        return True, 'sucesso.'
    
    except Exception as erro:
        return False, erro
    
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
        email = Email(destinatario,assunto, corpo)
        serverEmail = ServidorEmail()
        serverEmail.enviarEmail(email=email)
        return True, f'email enviado com sucesso para {destinatario}'
        
    
    except Exception as erro:
        return False, erro