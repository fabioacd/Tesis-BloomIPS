from django.urls import path
from apps.evento_adverso.views import index
from apps.evento_adverso.views import agregar_implicado_evento_adverso, modificar_implicado_evento_adverso, consultar_implicados_evento_adverso, \
    agregar_evento_adverso, consultar_evento, modificar_evento, registrar_protocolo, visualizar_protocolo, agregar_seguimiento, get_seguimientos_ajax, registrar_seguimiento_ajax


urlpatterns = [
    path('', index, name='index'),
    path('agregar_implicado_evento/', agregar_implicado_evento_adverso, name='agregar_implicado_evento_adverso'),
    path('modificar_implicado_evento/<id_implicado>/', modificar_implicado_evento_adverso, name='modificar_implicado_evento_adverso'),
    path('consultar_implicados_evento/', consultar_implicados_evento_adverso, name='consultar_implicados_evento_adverso'),
    path('agregar_evento_adverso/', agregar_evento_adverso, name='agregar_evento_adverso'),
    path('consultar_evento_adverso/', consultar_evento, name='consultar_evento'),
    path('modificar_evento_adverso/<id_evento>/', modificar_evento, name='modificar_evento'),
    path('registrar_protocolo_londres/<id_evento>/', registrar_protocolo, name='registrar_protocolo'),
    path('visualizar_protocolo_londres/<id_evento>/', visualizar_protocolo, name='visualizar_protocolo'),
    path('ajax/', get_seguimientos_ajax, name='get_seguimientos_ajax'),
    path('ajax-registrar/', registrar_seguimiento_ajax, name='agregar_seguimientos_ajax'),
path('agregar_seguimiento_evento/<id_evento>/', agregar_seguimiento, name='agregar_seguimiento'),
]

