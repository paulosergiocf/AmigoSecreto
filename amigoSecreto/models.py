from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password, check_password


class Participante(models.Model):
    """
    Representa cada participante que sera participara de algum sorteio de amigo secreto.
    """
    nome = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=False, max_length=320, unique=True)
    
    def __str__(self):
        return self.nome
    

class ResponsavelSala(AbstractUser):
    """
    Criador da sala que ficará responsável por:
    - Gerenciar parâmetros.
    - Aprovar participantes.
    """
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(blank=False, max_length=320, unique=True)
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
class Sala(models.Model):
    """ 
    Cria uma sala
    """
    codigoSala = models.CharField(max_length=20, unique=True)
    responsavelSala = models.ForeignKey(ResponsavelSala, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.codigoSala

class SalaParticipante(models.Model):
    """
    Vincula um participante a uma sala.
    """
    codigoSala = models.ForeignKey(Sala, on_delete=models.CASCADE, unique=False)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE, unique=False)
    valido = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.participante}"

class SalaSorteio(models.Model):
    """ Parametros para funcionamento da sala
    """
    codigoSala = models.ForeignKey(Sala, on_delete=models.CASCADE, unique=True)
    dataSorteio = models.DateField()
    valorMaximoPresente = models.FloatField(default=0.0)
    situacao = models.BooleanField(default=True)
    
    def __str__(self):
        return self.dataSorteio.strftime('%Y-%m-%d')
    
