from django.urls import path
from apps.paciente.views import registrar_paciente, consultar_paciente, ver_paciente, modificar_paciente, \
    agregar_evolucion_diaria, consultar_evolucion_diaria, get_evo_diaria_ajax

urlpatterns = [
    path('registrar_paciente/', registrar_paciente, name='registrar_paciente'),
    path('consultar_paciente/', consultar_paciente, name='consultar_paciente'),
    path('ver_paciente/<id_paciente>/', ver_paciente, name='ver_paciente'),
    path('modificar_paciente/<id_paciente>/', modificar_paciente, name='modificar_paciente'),
    path('agregar_evolucion_diaria/', agregar_evolucion_diaria, name='agregar_evolucion_diaria'),
    path('consultar_evolucion_diaria/', consultar_evolucion_diaria, name='consultar_evolucion_diaria'),
    path('ajax_evo_diaria/', get_evo_diaria_ajax, name='get_evo_diaria_ajax'),
]
