from django.db import models

class Participante(models.Model):
    """
    Representa cada participante que sera participara de algum sorteio de amigo secreto.
    """
    nome = models.CharField(max_length=50)
    email = models.EmailField(blank=False, max_length=30, unique=True)
    
    def __str__(self):
        return self.nome
    

class ResponsavelSala(Participante):
    """
    Criador da sala que ficará responsavel por:
    - Gerenciar parametros.
    - Aprovar participantes.
    """
    senha = models.CharField(max_length=32)
    
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
    
