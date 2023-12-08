from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.db.models import F
from django.contrib.auth import logout, authenticate, login
from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaSorteio, SalaParticipante
from amigoSecreto.forms import ParticipanteForm, ResponsavelSalaForm, SalaForm, SalaSorteioForm
from amigoSecreto.Messages import Mensagens
from amigoSecreto.usecases.utils import gerarDiagramacao
from amigoSecreto.usecases.regras import adicionarParticipanteSala, emailParticipanteCadastrado, adicionarParticipanteResponsavelSala, emailParticipanteResponsavelCadastrado
from amigoSecreto.usecases.sortear import executarSorteio

# ---------------- Paginas publicas-------------------
def index(request):
    """
    Busca todas as salas no banco de dados e cria um meno na pagina inicial para elas.
    """
    version = Mensagens.VERSION.value
    salas = Sala.objects.all()
    diagramacao = gerarDiagramacao(salas)
    return render(request, 'index.html', {'version':version,'diagramacao': diagramacao})

def sala(request, codigo):
    """
    
    Args:
    - codigo: string
    
    Descrição:
    Recebe o código da sala, pega os parametros, 
    participantes no banco de dados e renderiza na tela as informações
    """
    version = Mensagens.VERSION.value
    
    parametros = SalaSorteio.objects.filter(codigoSala__codigoSala=codigo)
    salaParticipantes = SalaParticipante.objects.filter(codigoSala__codigoSala=codigo)
    participantes = Participante.objects.filter(salaparticipante__in=salaParticipantes).annotate(valido=F('salaparticipante__valido')).values('nome', 'email', 'valido')
    sala = Sala.objects.get(codigoSala=codigo)
    responsavel = ResponsavelSala.objects.get(id=sala.responsavelSala.id)    
    usuariologado = None
    if request.user.is_authenticated:
        usuariologado = ResponsavelSala.objects.get(username=request.user)
        
    return render(request, 'sala.html', {'version':version,'codigo':codigo,'participantes':participantes, 'parametros':parametros,'usuariologado':usuariologado, 'responsavel':responsavel})

# Formulários
@csrf_protect
def participar(request, codigo):
    version = Mensagens.VERSION.value
    participante = None
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        sala = Sala.objects.get(codigoSala=codigo)
        email = request.POST.get('email')
        email = email.lower()
        if form.is_valid():
            participante_existente = Participante.objects.filter(email=email).exists()
            if participante_existente:
                participante = Participante.objects.filter(email=request.POST.get('email'))
            
            else:
                participante = form.save()
                
            
            retorno, mensagem = adicionarParticipanteSala(participante.nome, participante.email, sala)
            
            messages.success(request, 'Participante adicionado com sucesso!') if retorno else messages.error(request, mensagem)
                
            if retorno:
                retornoEmail, mensagemEmail = emailParticipanteCadastrado(participante, codigo)
                messages.success(request, mensagemEmail) if retornoEmail else messages.error(request, mensagemEmail)
                
            return redirect('sala',codigo)
        
            
        else:
            messages.warning(request, 'Digite e confira dos dados com atenção')
            
            
        
    else:
        form = ParticipanteForm(initial={'codigo': codigo})
        
        
    return render(request, 'participar.html', {'version':version,'codigo':codigo, 'form': form})

@csrf_protect
def criarSala(request):
    if not request.user.is_authenticated:
        messages.error(request, Mensagens.LOGIN_CRIAR_SALAS.value )
        return redirect('login')
    
    version = Mensagens.VERSION.value
    codigo = request.POST.get('codigoSala')
    data = request.POST.get('dataSorteio')
    valor = request.POST.get('valorMaximoPresente')
    
    if request.method == 'POST':
        try:
            responsavel = ResponsavelSala.objects.get(username=request.user)
            formSala = SalaForm({'codigoSala':codigo, 'responsavelSala':responsavel})
            
            criacaoSala = False
            criacaoParametros = False
            
            if formSala.is_valid():
                formSala.save()
                criacaoSala = True
            
            else:
                messages.error(request, "Código de Sala inválida.")
                
            sala = Sala.objects.get(codigoSala=codigo)
            
            formSalaSorteio = SalaSorteioForm({
                'codigoSala':sala,
                'dataSorteio':data,
                'valorMaximoPresente':valor,
                'situacao':True})
                
            if formSalaSorteio.is_valid() and criacaoSala:
                formSalaSorteio.save()
                criacaoParametros = True

            else:
                messages.error(request, "Parametros de Sorteio inválidos, defina-os novamente!")
            
            if criacaoSala and criacaoParametros:
                retorno, mensagem = adicionarParticipanteResponsavelSala(responsavel, sala)
                messages.success(request, 'você foi adicionado como participante!') if retorno else messages.error(request, mensagem)
            
        except Exception as erro:
            messages.error(request, erro)
        else:
            messages.success(request, 'Sala eParametros criados com sucesso!')
            return redirect('sala', codigo=codigo)
    
    return render(request, 'criarSala.html', {'version':version})

def aprovarParticipante(request, codigo, participante):
    if not request.user.is_authenticated:
        messages.error(request, Mensagens.LOGIN_CRIAR_SALAS.value)
        return redirect('login')
    version = Mensagens.VERSION.value
    sala_participante = SalaParticipante.objects.get(codigoSala__codigoSala=codigo, participante__email=participante)
    sala_participante.valido = True
    sala_participante.save()
    return redirect('sala', codigo=codigo)

@csrf_protect
def criarResponsavelSala(request):
    """
    Cria um ResponsavelSala com base nos parâmetros fornecidos.
    Retorna a instância do ResponsavelSala criada.
    """
    version = Mensagens.VERSION.value
    if request.method == 'POST':
        try:
            responsavelSala = ResponsavelSalaForm(request.POST)
            if responsavelSala.is_valid():
                    responsavelSala.save()
                    messages.success(request, 'Responsavel criado com sucesso, faça login para continuar')
                    
                    emailParticipanteResponsavelCadastrado(responsavelSala);
                    
                    return redirect('login')
                        
            else:
                messages.warning(request, 'Digite e confira dos dados com atenção')
        except Exception as erro:
                messages.warning(request, erro)
    else:
        form = ResponsavelSalaForm()
    return render(request, 'criarResponsavel.html',{'version':version})

def adminPagina(request):
    if not request.user.is_authenticated:
        messages.error(request, Mensagens.LOGIN_CRIAR_SALAS.value)
        return redirect('login')
    version = Mensagens.VERSION.value
    
    responsavel = ResponsavelSala.objects.get(username=request.user)
    salas = Sala.objects.filter(responsavelSala=responsavel)
    diagramacao = gerarDiagramacao(salas)
    return render(request, 'adminPagina.html', {'version':version,'diagramacao':diagramacao})

def sortear(request, codigo):
    if not request.user.is_authenticated:
        messages.error(request, Mensagens.LOGIN_CRIAR_SALAS.value )
        return redirect('login')
    
    version = Mensagens.VERSION.value
    
    responsavel = ResponsavelSala.objects.get(username=request.user)
    
    participantes = Participante.objects.filter(
        salaparticipante__codigoSala__codigoSala=codigo,
        salaparticipante__valido=True
    )
    sala = Sala.objects.get(codigoSala=codigo)
    if responsavel == sala.responsavelSala:
        retorno = executarSorteio(participantes)        
        messages.success(request, "Sorteio conclúido com sucesso") if retorno else messages.error(request, retorno)
    else:
        messages.error(request, "Somente o responsavel da sala pode efetuar o sorteio!")
    
    return redirect('sala', codigo=codigo)

# Gerenciar acessos
@csrf_protect
def efetuarlogin(request):
    version = Mensagens.VERSION.value
    if request.method == 'POST':
        username = request.POST.get('username', None).lower()
        senha = request.POST.get('senha')
        
        try:
            usuario = authenticate(request, username=username, password=senha)
            print(usuario)
            if usuario is not None:
                login(request, usuario)
                return redirect('adminPagina')
            else:
                messages.warning(request, "Credenciais inválidas.")
        except AuthenticationFailed as auth_failed:
            messages.warning(request, str(auth_failed))
            # Adicione logs para depuração
            # logger.error(f"Authentication failed: {auth_failed}")
        except Exception as erro:
            messages.warning(request, str(erro))
            # Adicione logs para depuração
            # logger.error(f"An unexpected error occurred: {erro}")
        finally:
            senha = email = None
            
    return render(request, 'login.html',{'version':version})

def efetuarlogout(request):
    """ Deslogar da página """
    logout(request)
    return redirect('login')

