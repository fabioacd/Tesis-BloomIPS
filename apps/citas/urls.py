from django.urls import path
from apps.citas.views import consultar_cita, agregar_cita, modificar_cita

urlpatterns = [
    path('consultar', consultar_cita, name='consultar_cita'),
    path('agregar', agregar_cita, name='agregar_cita'),
    path('modificar/<id_cita>/', modificar_cita, name='modificar_cita'),
]
