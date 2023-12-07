# forms.py
from django import forms
from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaSorteio
from django.core.exceptions import ValidationError

from amigoSecreto.usecases.utils import formatar

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email']
        
        
    def clean_email(self):
        """        
        Raises:
            ValidationError: Lança uma exção caso o email não tenha um domínio conhecido.
        """
        
        email = self.cleaned_data['email']
        email = email.lower()

        servidores = ['@gmail', '@protonme','@protonmail', '@hotmail', '@outlook', '@yahoo']
        if not any(servidor in email for servidor in servidores):
            raise ValidationError('O e-mail deve ter um dos seguintes domínios: @gmail, @proton.me, @protonmail, @hotmail, @outlook, @yahoo.')
        

        return email
    
    
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
        
    def clean_email(self):
        email = self.cleaned_data['email']
        return validarEmail(email)
    
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

def validarEmail(email: str):
        """        
        Raises:
            ValidationError: Lança uma exção caso o email não tenha um domínio conhecido.
        """
        validar_email = email.lower().strip()

        servidores = ['@gmail', '@proton.me','@protonmail', '@hotmail', '@outlook', '@yahoo']
        if not any(servidor in validar_email for servidor in servidores):
            raise ValidationError('O e-mail deve ter um dos seguintes domínios: @gmail, @proton.me, @protonmail, @hotmail, @outlook, @yahoo.')

        return validar_email
