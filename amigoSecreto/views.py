from django.shortcuts import render, redirect
from django.contrib import messages
from amigoSecreto.forms import ParticipanteForm
from amigoSecreto.models import Participante, ParametrosDoSorteio

# Create your views here.
def index(request):
    participantes = Participante.objects.all()
    parametros = ParametrosDoSorteio.objects.all()
    
    return render(request, 'index.html', {'participantes':participantes, 'parametros':parametros})

def participar(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()  # Isso salva os dados no banco de dados
            return redirect('index')  # Redireciona para uma página de sucesso
        else:
             messages.warning(request, 'Digite e confira dos dados com atenção')
    else:
        form = ParticipanteForm()
    return render(request, 'participar.html', {'form': form})