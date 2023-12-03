from django.urls import path
from amigoSecreto.views import index, participar, sala, criar_sala_sorteio, login, adminPagina,logout
from amigoSecreto.models import ResponsavelSala
urlpatterns = [
    path('', index, name='index'),
    path('sala/<str:codigo>/participar/', participar, name='participar'),
    path('sala/<str:codigo>/', sala, name='sala'),
    path('criar_sala_sorteio/', criar_sala_sorteio, name='criar_sala_sorteio'),
    path('login/', login, name='login'),
    path('adminPagina/<usuario>', adminPagina, name='adminPagina'),
    path('logout/', logout, name='logout'),
]