from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from amigoSecreto.context_processors import user_info
from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaSorteio, SalaParticipante
from amigoSecreto.usecases.enviar_email import ServidorEmail
from amigoSecreto.usecases.utils import usuario_esta_autenticado, Login_usuario, logout_usuario,compactarTextoURL, descompactarTextoURL
from amigoSecreto.forms import ParticipanteForm, ResponsavelSalaForm
from amigoSecreto.entities.email import Email
from amigoSecreto.Messages import Mensagens

global usuario


def index(request):
    """
    Busca todas as salas no banco de dados e cria um meno na pagina inicial para elas.
    """
    salas = Sala.objects.all()
    return render(request, 'index.html', {'salas': salas})

def sala(request, codigo):
    """
    
    Args:
    - codigo: string
    
    Descrição:
    Recebe o código da sala, pega os parametros, 
    participantes no banco de dados e renderiza na tela as informações
    """
    
    parametros = SalaSorteio.objects.filter(codigoSala__codigoSala=codigo)
    salaParticipantes = SalaParticipante.objects.filter(codigoSala__codigoSala=codigo)
    participantes = Participante.objects.filter(salaparticipante__in=salaParticipantes).annotate(valido=F('salaparticipante__valido')).values('nome', 'email', 'valido')
    
    return render(request, 'sala.html', {'codigo':codigo,'participantes':participantes, 'parametros':parametros})

@csrf_protect
def participar(request, codigo):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save() 
            sala = Sala.objects.get(codigoSala=codigo)
            participante = Participante.objects.get(email=participante.email)
            novo_participante_sala = SalaParticipante(codigoSala=sala, email=participante, valido=False)
            novo_participante_sala.save()
            
            messages.success(request, 'Participante adicionado com sucesso!')
            destinatario = participante.email
            assunto = f"Email - inscrição amigo secreto Sala {codigo}"
            corpo = Mensagens.EMAIL_PENDENTE.value
            corpo = corpo.replace("####",participante.nome).replace("$$$$", codigo)
            
            # email = Email(destinatario,assunto, corpo)
            # serverEmail = ServidorEmail()
            # serverEmail.enviarEmail(email=email)
            
            return redirect('sala',codigo)
        else:
            messages.warning(request, 'Digite e confira dos dados com atenção')
    else:
        form = ParticipanteForm(initial={'codigo': codigo})
    return render(request, 'participar.html', {'codigo':codigo, 'form': form})


@csrf_protect
def criar_sala_sorteio(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', None)
        requisicaoResponsavel = {
            'csrfmiddlewaretoken':request.POST.get('csrfmiddlewaretoken', None),
            'nome':request.POST.get('nome', None),
            'email':request.POST.get('email', None),
            'senha':request.POST.get('senha', None),
        }
        responsavelSala = ResponsavelSalaForm(requisicaoResponsavel)
      
        if responsavelSala.is_valid():
            responsavelSala.save()
            participante = ResponsavelSala.objects.get(email=str(requisicaoResponsavel['email']).lower())
            sala = Sala(codigoSala=codigo, responsavelSala=participante)
            sala.save()
            novo_participante_sala = SalaParticipante(codigoSala=sala, email=participante, valido=True)
            novo_participante_sala.save()
            messages.success(request, 'Responsavel e Sala criados com sucesso')
            return redirect('index.html')
        else:
            messages.warning(request, 'Digite e confira dos dados com atenção')
    else:
        form = ResponsavelSalaForm()
    return render(request, 'criar-sala.html')


def adminPagina(request, usuario):
    
    adminsalas = ResponsavelSala.objects.filter(nome=usuario)
  
    salas = None
    if usuario_esta_autenticado(request):
        return render(request, 'adminPagina.html',{'usuario':usuario,'salas':salas})
    else:
        return redirect('login')
    
@csrf_protect
def login(request):
    if usuario_esta_autenticado(request):
        usuario = user_info(request).get('user').username
        return redirect('adminPagina', usuario)
    
    
    email = request.POST.get('email', None)
    senha=request.POST.get('senha', None)
    
    if request.method == 'POST':
        try:
            usuario = ResponsavelSala.objects.get(email=email)
            if usuario.check_password(senha):
                Login_usuario(request, usuario)
                
                return redirect('adminPagina', usuario)
            else:
                messages.warning(request, "Credenciais inválidas.")
        except ResponsavelSala.DoesNotExist:
            messages.warning(request, "Usuário não encontrado.")
       
    return render(request, 'login.html')

def logout(request):
    logout_usuario(request)
    return redirect('login')