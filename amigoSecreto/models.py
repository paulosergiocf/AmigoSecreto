from django.db import models


class Participante(models.Model):
    
    nome = models.CharField(max_length=50)
    email = models.EmailField(blank=False, max_length=30, unique=True)
    valido = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome
    
class ParametrosDoSorteio(models.Model):

    data_sorteio = models.DateField()
    valorMaximoPresente = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.data_sorteio.strftime('%Y-%m-%d')
    
    


