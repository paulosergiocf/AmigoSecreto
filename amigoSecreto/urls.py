from django.urls import path
from amigoSecreto.views import index, participar

urlpatterns = [
    path('', index, name='index'),
    path('participar', participar, name='participar'),
]