from django.contrib import admin
from amigoSecreto.models import Participante, ParametrosDoSorteio

# Register your models here.
class Participantes(admin.ModelAdmin):
    list_display = ('id','nome','email','valido')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_per_page = 20
    
admin.site.register(Participante, Participantes)

class ParametrosDoSorteios(admin.ModelAdmin):
    list_display = ('id','data_sorteio','valorMaximoPresente')
    list_display_links = ('id', )

admin.site.register(ParametrosDoSorteio, ParametrosDoSorteios)