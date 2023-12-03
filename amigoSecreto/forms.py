# forms.py
from django import forms
from amigoSecreto.models import Participante, ResponsavelSala, Sala, SalaParticipante
from django.core.exceptions import ValidationError

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

        servidores = ['@gmail', '@proton.me','@protonmail', '@hotmail', '@outlook', '@yahoo']
        if not any(servidor in email for servidor in servidores):
            raise ValidationError('O e-mail deve ter um dos seguintes domínios: @gmail, @proton.me, @protonmail, @hotmail, @outlook, @yahoo.')


        return email
    
    def clean_nome(self):
        """
        Formata nome recebido para salvar como a primeira letra maiuscula no banco de dados.
        """
        nome = self.cleaned_data['nome']
        nome = nome.title()
        
        return nome
    
    
class ResponsavelSalaForm(forms.ModelForm):
    class Meta:
        model = ResponsavelSala
        fields = ['nome', 'email','senha']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        return validarEmail(email)
    
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['codigoSala', 'responsavelSala']
        
    
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
