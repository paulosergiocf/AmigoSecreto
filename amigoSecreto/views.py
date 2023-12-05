from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import F
from django.contrib.auth import logout, authenticate, login
from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaSorteio, SalaParticipante
from amigoSecreto.usecases.enviar_email import ServidorEmail
from amigoSecreto.forms import ParticipanteForm, ResponsavelSalaForm, SalaForm, SalaSorteioForm
from amigoSecreto.entities.email import Email
from amigoSecreto.Messages import Mensagens
from amigoSecreto.usecases.utils import gerarDiagramacao

# Paginas publicas
def index(request):
    """
    Busca todas as salas no banco de dados e cria um meno na pagina inicial para elas.
    """
    salas = Sala.objects.all()
    diagramacao = gerarDiagramacao(salas)
    return render(request, 'index.html', {'diagramacao': diagramacao})

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
    sala = Sala.objects.get(codigoSala=codigo)
    responsavel = ResponsavelSala.objects.get(id=sala.responsavelSala.id)    
    usuariologado = None
    if request.user.is_authenticated:
        usuariologado = ResponsavelSala.objects.get(username=request.user)
        
    return render(request, 'sala.html', {'codigo':codigo,'participantes':participantes, 'parametros':parametros,'usuariologado':usuariologado, 'responsavel':responsavel})

# Formulários
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
            
            email = Email(destinatario,assunto, corpo)
            serverEmail = ServidorEmail()
            serverEmail.enviarEmail(email=email)
            
            return redirect('sala',codigo)
        else:
            messages.warning(request, 'Digite e confira dos dados com atenção')
    else:
        form = ParticipanteForm(initial={'codigo': codigo})
    return render(request, 'participar.html', {'codigo':codigo, 'form': form})

@csrf_protect
def criarSala(request):
    messages.error(request, "Pagina não funcional ainda, por favor aguarde.")
    if not request.user.is_authenticated:
        messages.error(request, 'É necessário fazer o login para criar salas.' )
        return redirect('login')
    
    codigo = request.POST.get('codigoSala')
    if request.method == 'POST':
        try:
            responsavel = ResponsavelSala.objects.get(username=request.user)
            formSala = SalaForm({'codigoSala':codigo, 'responsavelSala':responsavel})
        
            formSalaSorteio = SalaSorteioForm(request.POST)
            if formSala.is_valid() and formSalaSorteio.is_valid():
                formSala.save()
                formSalaSorteio.save()
                messages.success(request, 'Sala e Parametros criados com sucesso!')
                
            else:
                messages.error(request, "Formulário inválido!")
            
        except Exception as erro:
            messages.error(request, erro)
    
    return render(request, 'criarSala.html')


def aprovarParticipante(request, codigo, participante):
    if not request.user.is_authenticated:
        messages.error(request, 'É necessário fazer o login para aprovar participante.' )
        return redirect('login')
    
    sala_participante = SalaParticipante.objects.get(codigoSala__codigoSala=codigo, email__email=participante)
    sala_participante.valido = True
    sala_participante.save()
    return redirect('sala', codigo=codigo)

@csrf_protect
def criarResponsavelSala(request):
    """
    Cria um ResponsavelSala com base nos parâmetros fornecidos.
    Retorna a instância do ResponsavelSala criada.
    """
    if request.method == 'POST':
        try:
            responsavelSala = ResponsavelSalaForm(request.POST)
            if responsavelSala.is_valid():
                    responsavelSala.save()
                    messages.success(request, 'Responsavel e Sala criados com sucesso')
                    
                    destinatario = responsavelSala.email
                    assunto = f"Criação de conta"
                    corpo = f"{responsavelSala.username} sua conta foi criada com sucesso!"
                    
                    email = Email(destinatario,assunto, corpo)
                    serverEmail = ServidorEmail()
                    serverEmail.enviarEmail(email=email)
                    
                    return redirect('login')
                

                
            else:
                messages.warning(request, 'Digite e confira dos dados com atenção')
        except Exception as erro:
                messages.warning(request, erro)
    else:
        form = ResponsavelSalaForm()
    return render(request, 'criarResponsavel.html')

def adminPagina(request):
    
    if not request.user.is_authenticated:
        messages.error(request, 'É necessário fazer o login para acessar a pagina de admin.' )
        return redirect('login')
    
    responsavel = ResponsavelSala.objects.get(username=request.user)
    salas = Sala.objects.filter(responsavelSala=responsavel)
    diagramacao = gerarDiagramacao(salas)
    return render(request, 'adminPagina.html', {'diagramacao':diagramacao})
    
    
    
# Gerenciar acessos
@csrf_protect
def efetuarlogin(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        try:
            usuario = authenticate(request, username=nome, password=senha)
            if usuario is not None:
                login(request, usuario)
                return redirect('adminPagina')
            else:
                messages.warning(request, "Credenciais inválidas.")
        except Exception as erro:
            messages.warning(request, erro)
    return render(request, 'login.html')

def efetuarlogout(request):
    """ Deslogar da página """
    logout(request)
    return redirect('login')