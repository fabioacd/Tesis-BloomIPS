from django.urls import path
from apps.evento_adverso.views import index
from apps.evento_adverso.views import agregar_implicado_evento_adverso, modificar_implicado_evento_adverso, consultar_implicados_evento_adverso


urlpatterns = [
    path('', index, name='index'),
    path('agregar_implicado_evento/', agregar_implicado_evento_adverso, name='agregar_implicado_evento_adverso'),
    path('modificar_implicado_evento/<id_implicado>/', modificar_implicado_evento_adverso, name='modificar_implicado_evento_adverso'),
    path('consultar_implicados_evento/', consultar_implicados_evento_adverso, name='consultar_implicados_evento_adverso'),
]

