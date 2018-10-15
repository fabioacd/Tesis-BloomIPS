from django.urls import path
from apps.evento_adverso.views import index
from apps.evento_adverso.views import agregar_implicado_evento_adverso


urlpatterns = [
    path('', index, name='index'),
    path('agregar_implicado_evento/', agregar_implicado_evento_adverso, name='agregar_implicado_evento_adverso'),
]

