from django.contrib import admin
from amigoSecreto.models import Participante, SalaSorteio, ResponsavelSala, Sala, SalaParticipante

# Register your models here.
class Participantes(admin.ModelAdmin):
    list_display = ('id','nome','email')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_per_page = 20
    
admin.site.register(Participante, Participantes)

class ResponsaveisSala(admin.ModelAdmin):
    list_display = ('id','nome','email','senha')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_per_page = 20
    
admin.site.register(ResponsavelSala, ResponsaveisSala)

class SalaDoSorteios(admin.ModelAdmin):
    list_display = ('id','codigoSala','dataSorteio','valorMaximoPresente','situacao')
    list_display_links = ('id', )

admin.site.register(SalaSorteio, SalaDoSorteios)

class Salas(admin.ModelAdmin):
    list_display = ('id','codigoSala','responsavelSala')
    list_display_links = ('id', )

admin.site.register(Sala, Salas)

class SalasParticipantes(admin.ModelAdmin):
    list_display = ('id','codigoSala','email','valido')
    list_display_links = ('id', )

admin.site.register(SalaParticipante, SalasParticipantes)