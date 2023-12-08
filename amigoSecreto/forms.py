# forms.py
from django import forms
from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaSorteio
from django.core.exceptions import ValidationError

from amigoSecreto.usecases.utils import formatar

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email']
        
        
    
    def clean_nome(self):
        """
        Formata nome recebido para salvar como a primeira letra maiuscula no banco de dados.
        """
        nome = f"{self.cleaned_data['nome']}"
        nome = nome.lower()
        
        return nome
    
    
class ResponsavelSalaForm(forms.ModelForm):
    class Meta:
        model = ResponsavelSala
        fields = ['username', 'email','password']
        

    def clean_nome(self):
        """
        Formata nome recebido para salvar como a primeira letra maiuscula no banco de dados.
        """
        username = f"{self.cleaned_data['username']}"
        username = username.lower()
        
        return username
    
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['codigoSala', 'responsavelSala']
        
    
class SalaSorteioForm(forms.ModelForm):
    class Meta:
        model = SalaSorteio
        fields = ['codigoSala', 'dataSorteio', 'valorMaximoPresente', 'situacao']
        
    
    
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['codigoSala', 'responsavelSala']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigoSala'].widget.attrs.update({'class': 'form-control'})

