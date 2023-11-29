from django.shortcuts import render, redirect
from django.contrib import messages
from amigoSecreto.forms import ParticipanteForm
from amigoSecreto.models import Participante, Sala, SalaSorteio, ResponsavelSala, SalaParticipante
from django.db.models import F

def index(request):
    salas = Sala.objects.all()
    return render(request, 'index.html', {'salas': salas})

def sala(request, codigo):
    
    parametros = SalaSorteio.objects.filter(codigoSala__codigoSala=codigo)
    salaParticipantes = SalaParticipante.objects.filter(codigoSala__codigoSala=codigo)
    participantes = Participante.objects.filter(salaparticipante__in=salaParticipantes).annotate(valido=F('salaparticipante__valido')).values('nome', 'email', 'valido')
    
    return render(request, 'sala.html', {'codigo':codigo,'participantes':participantes, 'parametros':parametros})
   
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
            return redirect('index')  # Redireciona para uma página de sucesso
        else:
            if not form.is_valid():
                print(form.errors)
            messages.warning(request, 'Digite e confira dos dados com atenção')
    else:
        form = ParticipanteForm(initial={'codigo': codigo})
    return render(request, 'participar.html', {'codigo':codigo, 'form': form})



def criar_sala_sorteio(request):
    
    return render(request, 'criar-sala.html')