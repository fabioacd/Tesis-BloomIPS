from django.urls import path
from apps.evento_adverso.views import agregar_evento_adverso, agregar_implicado_evento_adverso, modificar_implicado_evento_adverso, consultar_implicados_evento_adverso, consultar_evento, \
    modificar_evento, agregar_seguimiento, get_seguimientos_ajax, registrar_protocolo, visualizar_protocolo, registrar_seguimiento_ajax, modificar_protocolo, ajax_filtro_consultar_implicado, \
    ajax_filtro_consultar_evento

urlpatterns = [
    path('agregar_evento_adverso/', agregar_evento_adverso, name='agregar_evento_adverso'),
    path('agregar_implicado_evento/', agregar_implicado_evento_adverso, name='agregar_implicado_evento_adverso'),
    path('modificar_implicado_evento/<id_implicado>/', modificar_implicado_evento_adverso, name='modificar_implicado_evento_adverso'),
    path('consultar_implicados_evento/', consultar_implicados_evento_adverso, name='consultar_implicados_evento_adverso'),
    path('consultar_evento_adverso/', consultar_evento, name='consultar_evento'),
    path('modificar_evento_adverso/<id_evento>/', modificar_evento, name='modificar_evento'),
    path('agregar_seguimiento_evento/<id_evento>/', agregar_seguimiento, name='agregar_seguimiento'),
    path('registrar_protocolo_londres/<id_evento>/', registrar_protocolo, name='registrar_protocolo'),
    path('modificar_protocolo_londres/<id_evento>/', modificar_protocolo, name='modificar_protocolo'),
    path('visualizar_protocolo_londres/<id_evento>/', visualizar_protocolo, name='visualizar_protocolo'),
    path('ajax/', get_seguimientos_ajax, name='get_seguimientos_ajax'),
    path('ajax-registrar/', registrar_seguimiento_ajax, name='agregar_seguimientos_ajax'),
    path('ajax_filtro_consultar_implicado/', ajax_filtro_consultar_implicado.as_view(), name='ajax_filtro_consultar_implicado'),
    path('ajax_filtro_consultar_evento adverso/', ajax_filtro_consultar_evento.as_view(), name='ajax_filtro_consultar_evento'),

]
