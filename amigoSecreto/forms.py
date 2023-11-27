# forms.py
from django import forms
from amigoSecreto.models import Participante
from django.core.exceptions import ValidationError

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'email']
        
    def clean_email(self):
        email = self.cleaned_data['email']

        # Adicione sua lógica de validação personalizada aqui
        servidores = ['@gmail', '@proton.me','@protonmail', '@hotmail', '@outlook', '@yahoo']
        if not any(servidor in email for servidor in servidores):
            raise ValidationError('O e-mail deve ter um dos seguintes domínios: @gmail, @proton.me, @protonmail, @hotmail, @outlook, @yahoo.')


        return email