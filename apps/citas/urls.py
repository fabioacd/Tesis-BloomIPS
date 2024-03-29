from django.urls import path
from apps.citas.views import consultar_cita, agregar_cita, modificar_cita, get_info_cita, cancelar_cita

urlpatterns = [
    path('consultar', consultar_cita, name='consultar_cita'),
    path('agregar', agregar_cita, name='agregar_cita'),
    path('modificar/<id_cita>/', modificar_cita, name='modificar_cita'),
    path('get_info_cita/', get_info_cita, name='get_info_cita'),
    path('cancelar_cita/', cancelar_cita, name='cancelar_cita')
]
