from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

class Participante(models.Model):
    """
    Representa cada participante que sera participara de algum sorteio de amigo secreto.
    """
    nome = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=False, max_length=30, unique=True)
    
    def __str__(self):
        return self.nome
    

class ResponsavelSala(Participante):
    """
    Criador da sala que ficará responsavel por:
    - Gerenciar parametros.
    - Aprovar participantes.
    """
    senha = models.CharField(max_length=128)
    def save(self, *args, **kwargs):
        self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)
    
class Sala(models.Model):
    """ 
    Cria uma sala
    """
    codigoSala = models.CharField(max_length=20)
    responsavelSala = models.ForeignKey(ResponsavelSala, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.codigoSala

class SalaParticipante(models.Model):
    """
    Vincula um participante a uma sala.
    """
    codigoSala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    email = models.ForeignKey(Participante, on_delete=models.CASCADE)
    valido = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.codigoSala}|{self.email}|{self.valido}"

class SalaSorteio(models.Model):
    """ Parametros para funcionamento da sala
    """
    codigoSala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    dataSorteio = models.DateField()
    valorMaximoPresente = models.FloatField(default=0.0)
    situacao = models.BooleanField(default=True)
    
    def __str__(self):
        return self.dataSorteio.strftime('%Y-%m-%d')
    
