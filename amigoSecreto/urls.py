from django.urls import path
from amigoSecreto.views import index, participar, sala, efetuarlogin, adminPagina,efetuarlogout, criarResponsavelSala, criarSala, aprovarParticipante

urlpatterns = [
    path('', index, name='index'),
    path('sala/<str:codigo>/participar/', participar, name='participar'),
    path('sala/<str:codigo>/', sala, name='sala'),
    path('cadastrar/', criarResponsavelSala, name='cadastrar'),
    path('login/', efetuarlogin, name='login'),
    path('logout/', efetuarlogout, name='logout'),
    path('adminPagina/', adminPagina, name='adminPagina'),
    path('adminPagina/criarsala', criarSala, name='criarsala'),
    path('adminPagina/<str:codigo>/aprovarParticipante/<str:participante>/', aprovarParticipante, name='aprovarParticipante'),
]